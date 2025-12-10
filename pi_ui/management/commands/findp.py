from pathlib import Path
from typing import override

from django.core.management.base import BaseCommand, CommandParser
from pi_py.algo.control import CONTROL_FILE

class Command(BaseCommand):
    help = f'Find pi palindrome in the control file - etc/pi-billion.txt'

    @override
    def add_arguments(self, parser: CommandParser) -> None:
        file_path = str(CONTROL_FILE)
        default_palindrome = '314151413'

        parser.add_argument(
            '-a',
            '--all',
            default=False,
            action='store_true',
            help=f'find all instances of the palindrome (default: {False})',
        )
        parser.add_argument(
            '-f',
            '--file',
            default=file_path,
            type=Path,
            help=f'file to read 1B digits of pi (default: {file_path})',
        )
        parser.add_argument(
            '-p',
            '--palindrome',
            default=default_palindrome,
            help=f'search for this palindrome (default: {default_palindrome})',
        )

    @override
    def handle(self, *args, **options) -> None:
        verbosity = options['verbosity']
        all = options['all'] or verbosity < 2

        file_path = Path(options['file'])
        if(verbosity >= 2):
            self.stdout.write(f'{file_path=} => {file_path.stat().st_size:_} bytes')

        pi_palindrome = options['palindrome']

        count: int = 0
        index: int = -1
        with open(file_path, 'r', encoding='ascii') as f:
            content = f.read()
            while (index := content.find(pi_palindrome, index + 1)) > -1:
                count += 1

                if verbosity >= 2:
                    self.stdout.write(f'{index:_}:\'{pi_palindrome}\'', self.style.SUCCESS)

                if not all:
                    break

        self.stdout.write(f'\'{pi_palindrome}\':{count:_}', self.style.SUCCESS)
