import json
from datetime import datetime
from pathlib import Path
from typing import Any

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

# from ...models import Author, Quote, Tag
from ... import models as postgres
from ..migration import Logger, Author, Quote, Tag, update_or_create

AUTHORS_FILE    = "authors.json"
QUOTES_FILE     = "quotes.json"

def seed(path):
    result =    {
                    "authors" : {
                        "created": 0,
                        "updated": 0,
                    },
                    "quotes" : {
                        "created": 0,
                        "updated": 0,
                        "skipped": 0,
                    },
                    "tags" : {
                        "created": 0,
                        "updated": 0,
                    },
                }

    admin  = User.objects.get(pk=1)
    py_logger = Logger(modified_by=admin)
    # py_logger.created_by   = admin
    # py_logger.modified_by  = admin

    # Process authors.
    filename = path / AUTHORS_FILE
    with open(filename) as fd:
        datas = json.load(fd)
    for data in datas:
        author = {}
        for key, value in data.items():
            if "date" in key:
                value = datetime.strptime(value, "%B %d, %Y").date()
            author[key] = value
        author["modified_by"] = admin

        pg_author, created = update_or_create(author, Author, postgres.Author)
        if created:
            result["authors"]["created"] += 1
        else:
            result["authors"]["updated"] += 1

    # Iterate through quotes.
    filename = path / QUOTES_FILE
    with open(filename) as fd:
        datas = json.load(fd)
    for data in datas:
        # Find author
        pg_author = postgres.Author.objects.filter(fullname=data["author"]).first()
        if pg_author is None:
            result["quotes"]["skipped"] += 1
            continue

        quote = {}
        for key, value in data.items():
            if "date" in key:
                value = datetime.strptime(value, "%B %d, %Y").date()
            quote[key] = value
        quote["modified_by"] = admin
        quote["author"] = pg_author

        pg_quote, created = update_or_create(quote, Quote, postgres.Quote)
        if created:
            result["quotes"]["created"] += 1
        else:
            result["quotes"]["updated"] += 1

        # Fill tags.
        tags = []
        for tag_name in data["tags"]:
            tag = {}
            tag["name"] = tag_name
            tag["modified_by"] = admin
            
            pg_tag, created = update_or_create(tag, Tag, postgres.Tag)
            if created:
                result["tags"]["created"] += 1
            else:
                result["tags"]["updated"] += 1

            tags.append(pg_tag)
            if not pg_quote.tags.contains(pg_tag):
                pg_quote.tags.add(pg_tag)
        # Remove old tags
        for tag in pg_quote.tags.all():
            if not tag in tags:
                pg_quote.tags.remove(tag)
    return result
    
class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any) -> str | None:
        # super().handle(*args, **options)
        app = __package__.split(".management.commands")[0].split('.')[-1]
        result = seed(options["data"] / "data")
        print(result)
        return

    def add_arguments(self, parser):
            parser.add_argument(
            '-d', 
            '--data',
            action='store', 
            default=Path.cwd(),
            help='Path to store JSON-data.'
        )
