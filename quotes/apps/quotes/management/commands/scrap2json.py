import shutil
from pathlib import Path
from typing import Any
from django.core.management.base import BaseCommand

from quotes_toscrape_com import spiders
from scrapper import scrapper

class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any) -> str | None:
        # super().handle(*args, **options)
        app = __package__.split(".management.commands")[0].split('.')[-1]
        data_path = options["data"] / "data"
        if data_path.exists():
            shutil.rmtree(data_path)
        _spiders = [spiders.AuthorsSpider, spiders.QuotesSpider]
        scrapper.scrap(_spiders)
        return

    def add_arguments(self, parser):
            parser.add_argument(
            '-d', 
            '--data',
            action='store', 
            default=Path.cwd(),
            help='Path to store JSON-data.'
        )
