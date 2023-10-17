from datetime import date
from pathlib import Path
from pydantic import BaseModel, ConfigDict
from typing import Any


from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist

from homework_8_1 import connection
from homework_8_1 import models as mongodb

from ... import models as postgres
from ..migration import Logger, Author, Quote, Tag, update_or_create



def migrate():
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

    admin  = postgres.User.objects.get(pk=1)
    # py_logger = Logger(modified_by=admin)
    # py_logger.created_by   = admin
    # py_logger.modified_by  = admin
    for mg_quote in mongodb.Quote.objects.all():
        mg_author = mg_quote.author
        if mg_author is None:
            result["quotes"]["skipped"] += 1
            continue

        pg_author, created = update_or_create(admin, mg_author, Author, postgres.Author)
        if created:
            result["authors"]["created"] += 1
        else:
            result["authors"]["updated"] += 1

        # mg_quote["modified_by"] = admin
        # mg_quote.extend("modified_by", admin)
        mg_quote.author = pg_author
        pg_quote, created = update_or_create(admin, mg_quote, Quote, postgres.Quote)
        if created:
            result["quotes"]["created"] += 1
        else:
            result["quotes"]["updated"] += 1

        # Fill tags.
        tags = []
        for mg_tag in mg_quote.tags:
            # mg_tag.extend("modified_by", admin)

            pg_tag, created = update_or_create(admin, mg_tag, Tag, postgres.Tag)
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
        result = migrate()
        print(result)
        return
