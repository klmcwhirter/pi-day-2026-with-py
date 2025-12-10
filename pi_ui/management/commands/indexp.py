from dataclasses import dataclass, field
from pathlib import Path
from pprint import pprint
from typing import Any, override

from django.core.management.base import BaseCommand, CommandParser

from pi_py.algo.control import CONTROL_FILE
from pi_py.utils import palindrome
from pi_ui.models import PiPosition

MAX_DIGITS = 20


@dataclass
class IndexContext:
    file_path: Path = field(default=CONTROL_FILE)
    pi_contents: str = field(default_factory=str)
    dry_run: bool = field(default=False)
    verbose: bool = field(default=False)
    misses: int = field(default=0)

    positions: list[dict[str, Any]] = field(init=False)

    def __post_init__(self) -> None:
        self.positions = []


def pi_from_file(file_path: Path) -> str:
    content: str = ''

    with open(file_path, 'r', encoding='ascii') as f:
        content = f.read()

    return '3' + content[2:]


class Command(BaseCommand):
    help = f'Index digits of pi by numeric palindromes'

    @override
    def add_arguments(self, parser: CommandParser) -> None:
        file_path = str(CONTROL_FILE)
        parser.add_argument(
            '-f',
            '--file',
            default=file_path,
            type=Path,
            help=f'file to read 1B digits of pi (default: {file_path})',
        )
        parser.add_argument(
            '-m',
            '--max',
            default=MAX_DIGITS,
            type=int,
            help=f'max digits of pi for which to search palindromes (default: {MAX_DIGITS})',
        )
        parser.add_argument(
            '-n',
            '--dry-run',
            default=False,
            action='store_true',
            help='Show what would be done but perform no desctructive actions (default: False)',
        )

    def _find_all_for(self, ctx: IndexContext, digits: str, pi_palindrome: str) -> None:
        count: int = 0
        index: int = 0

        if ctx.verbose:
            self.stdout.write(f'\'{pi_palindrome}\'', self.style.MIGRATE_HEADING)

        while True:
            index = ctx.pi_contents.find(pi_palindrome, index + 1)

            if index < 0:
                if count == 0:
                    ctx.misses += 1
                if ctx.verbose:
                    self.stdout.write(f'MISS:\'{pi_palindrome}\'', self.style.WARNING)
                break

            count += 1
            ctx.misses = 0

            ctx.positions.append({
                'idx': index,
                'digits': digits,
                'palindrome': pi_palindrome
            })

            if ctx.verbose:
                self.stdout.write(f'{index:_}:\'{pi_palindrome}\'', self.style.SUCCESS)

        self.stdout.write(f'\'{pi_palindrome}\':{count:_}', self.style.SUCCESS)

    def _find_all_palindromes(self, ctx: IndexContext, digits: str) -> None:
        for pi_palindrome in (palindrome(digits=digits), palindrome(digits=digits, double_middle=True)):
            # self.stdout.write(f'\'{pi_palindrome}\'', self.style.MIGRATE_LABEL)
            self._find_all_for(ctx, digits, pi_palindrome=pi_palindrome)

    @override
    def handle(self, *args, **options) -> None:
        file_path = Path(options['file'])
        dry_run = options['dry_run']
        verbosity = options['verbosity']

        ctx = IndexContext(
            file_path=file_path,
            pi_contents=pi_from_file(file_path),
            dry_run=dry_run,
            verbose=verbosity >= 2
        )

        if (ctx.verbose):
            self.stdout.write(f'{file_path=} => {file_path.stat().st_size:_} bytes')

        for digits in [ctx.pi_contents[:n] for n in range(3, options['max'] + 1)]:
            self._find_all_palindromes(ctx=ctx, digits=digits)

        self.stdout.write(f'\'{len(ctx.positions)=}\'', self.style.SUCCESS)

        if not ctx.dry_run:
            self.load_positions(ctx)

    def load_positions(self, ctx: IndexContext) -> None:
        # clear table
        PiPosition.objects.all().delete()

        PiPosition.objects.bulk_create(
            PiPosition(idx=p['idx'], palindrome=p['palindrome'], digits=p['digits'])
            for p in ctx.positions
        )

        self.stdout.write(f'\'{PiPosition.objects.count()=}\'', self.style.SUCCESS)
