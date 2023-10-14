from pathlib import Path
from typing import Any

from django.core.management.base import BaseCommand

from homework_8_1 import connection
from homework_8_1 import seed



class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any) -> str | None:
        # super().handle(*args, **options)
        app = __package__.split(".management.commands")[0].split('.')[-1]
        seed.seed(options["data"] / "data")
        return

    def add_arguments(self, parser):
            parser.add_argument(
            '-d', 
            '--data',
            action='store', 
            default=Path.cwd(),
            help='Path to store JSON-data.'
        )
