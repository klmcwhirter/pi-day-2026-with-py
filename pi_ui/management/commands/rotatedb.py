import os
import shutil
from pathlib import Path

from django.core.management.base import BaseCommand, CommandParser

from pi_site.settings import DB_ROTATE_COUNT, DB_PATH


class Command(BaseCommand):
    help = f'Rotate the sqlite3 files in {os.path.dirname(DB_PATH)} over {DB_ROTATE_COUNT} files'

    def add_arguments(self, parser: CommandParser) -> None:
        db_path_basename = os.path.basename(DB_PATH)
        parser.add_argument(
            '-r',
            '--reverse',
            default=False,
            action='store_true',
            help=f"""
                Reverses a rotatedb operation:
                removes {db_path_basename}
                and copies starting at {db_path_basename}.01 up to {db_path_basename}.{DB_ROTATE_COUNT - 1:02d};
                does nothing (with warning) if no backups are available (i.e., {db_path_basename}.01 does not exist)
                """,
        )

    def _handle_reverse(self, *args, **options) -> None:
        db_filepath = DB_PATH

        self.stdout.write('Reverse rotating db backup files ...', self.style.MIGRATE_HEADING)

        old = f'{db_filepath}.01'
        if os.path.exists(old):
            # remove curr file
            self.stdout.write(f'Removing {db_filepath}', self.style.MIGRATE_LABEL)
            os.remove(db_filepath)

            # rename .01 to db_filepath
            self.stdout.write(f'Renaming {old} to {db_filepath}', self.style.MIGRATE_LABEL)
            os.rename(old, db_filepath)

            # reverse rotate all others
            for ct in range(1, DB_ROTATE_COUNT + 1):
                old = f'{db_filepath}.{ct + 1:02d}'
                if os.path.exists(old):
                    new = f'{db_filepath}.{ct:02d}'
                    self.stdout.write(f'{old} exists - renaming to {new}', self.style.MIGRATE_LABEL)
                    os.rename(old, new)
                else:
                    self.stdout.write(f'{old} does not exist - stopping', self.style.NOTICE)
                    break
        else:
            self.stdout.write(f'{old} does not exist - nothing to do', self.style.NOTICE)

        self.stdout.write('Done reverse rotating db backup files ...', self.style.SUCCESS)

    def _handle_forward(self, *args, **options) -> None:
        db_filepath = DB_PATH

        self.stdout.write('Rotating db backup files ...', self.style.MIGRATE_HEADING)

        if os.path.exists(db_filepath):
            # if exists, delete 10th copy
            old = f'{db_filepath}.{DB_ROTATE_COUNT}'
            if os.path.exists(old):
                self.stdout.write(f'{old} exists - removing', self.style.NOTICE)
                os.remove(old)
            else:
                self.stdout.write(f'{old} does not exist - skipping', self.style.NOTICE)

            # rotate all others
            for ct in reversed(range(1, DB_ROTATE_COUNT)):
                old = f'{db_filepath}.{ct:02d}'
                if os.path.exists(old):
                    new = f'{db_filepath}.{ct + 1:02d}'
                    self.stdout.write(f'{old} exists - renaming to {new}', self.style.MIGRATE_LABEL)
                    os.rename(old, new)
                else:
                    self.stdout.write(f'{old} does not exist - skipping', self.style.NOTICE)

            # copy current
            new = f'{db_filepath}.01'
            self.stdout.write(f'Copying {db_filepath} to {new}', self.style.MIGRATE_LABEL)
            shutil.copy2(db_filepath, new)

            # touch current
            Path(db_filepath).touch(exist_ok=True)
        else:
            self.stdout.write(f'{db_filepath} does not exist - nothing to do', self.style.NOTICE)

        self.stdout.write('Done rotating db backup files ...', self.style.SUCCESS)

    def handle(self, *args, **options) -> None:
        if 'reverse' in options and options['reverse']:
            self._handle_reverse(*args, **options)
        else:
            self._handle_forward(*args, **options)
