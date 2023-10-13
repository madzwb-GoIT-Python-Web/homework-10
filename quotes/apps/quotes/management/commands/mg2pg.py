from datetime import date
from pathlib import Path
from pydantic import BaseModel, ConfigDict
from typing import Any


from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist

from homework_8_1 import connection
from homework_8_1 import models as mongodb

from ... import models as postgres#import Author, Tag, Quote



class Logger(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

    created_by      : postgres.User|None = None
    modified_by     : postgres.User|None = None



class Author(Logger):
    fullname        : str
    born_date       : date
    born_location   : str
    description     : str



class Quote(Logger):
    author      : postgres.Author|mongodb.Author|None = None
    quote       : str
    # tags        : list[str]



class Tag(Logger):
    name        : str



def migrate():
    authors_created = 0
    authors_updated = 0
    quotes_created  = 0
    quotes_updated  = 0
    quotes_skipped  = 0
    tags_created    = 0
    tags_updated    = 0

    admin  = postgres.User.objects.get(pk=1)
    for mg_quote in mongodb.Quote.objects.all():#mongodb.Quote.objects().all():
        mg_author = mg_quote.author
        if mg_author is None:
            quotes_skipped += 1
            continue
        py_logger = Logger()
        py_logger.created_by   = admin
        py_logger.modified_by  = admin

        py_author = Author.model_validate(mg_author)
        author = py_author.model_dump()
        author.update(py_logger)
        pg_author, created  =   postgres.Author.objects.update_or_create(
                                    fullname=py_author.fullname,
                                    defaults=author,
                                )
        if created:
            authors_created += 1
        else:
            authors_updated += 1
        # try:
        #     pg_author = postgres.Author.objects.get(fullname=mg_author.fullname)
        # except ObjectDoesNotExist:
        #     pg_author = postgres.Author.objects.create(**author)
        py_quote = Quote.model_validate(mg_quote)
        py_quote.author = pg_author
        quote = py_quote.model_dump()
        quote.update(py_logger)
        pg_quote, created   =   postgres.Quote.objects.update_or_create(
                                    quote       = py_quote.quote,
                                    defaults    = quote,
                                )
        if created:
            quotes_created += 1
        else:
            quotes_updated += 1
        for mg_tag in mg_quote.tags:
            py_tag = Tag.model_validate(mg_tag)
            tag = py_tag.model_dump()
            tag.update(py_logger)
            pg_tag, created =   postgres.Tag.objects.update_or_create(
                                    name        = py_tag.name,
                                    defaults    = tag,
                                )
            if created:
                tags_created += 1
            else:
                tags_updated += 1
            pg_quote.tags.add(pg_tag)

    return  {
                "authors" : {
                    "created": authors_created,
                    "updated": authors_updated,
                },
                "quotes" : {
                    "created": quotes_created,
                    "updated": quotes_updated,
                    "skipped": quotes_skipped,
                },
                "tags" : {
                    "created": tags_created,
                    "updated": tags_updated,
                },
            }

class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any) -> str | None:
        # super().handle(*args, **options)
        app = __package__.split(".management.commands")[0].split('.')[-1]
        result = migrate()
        print(result)
        return
