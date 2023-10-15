import json
from datetime import datetime
from pathlib import Path
from typing import Any

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

# from ...models import Author, Quote, Tag
from ... import models as postgres
from ..migration import Logger, Author, Quote, Tag

AUTHORS_FILE    = "authors.json"
QUOTES_FILE     = "quotes.json"

def update_or_create(user, data, PYModel, PGModel):
    # result = {
    #     "created"   : 0,
    #     "updated"   : 0,
    #     "skipped"   : 0,
    # }
    py_model = PYModel.model_validate(data)

    uniques = [f for f in PGModel._meta.fields if f.unique]
    params = {u.name: data[u.name] for u in uniques if u.name in data}

    try:
        created = False
        pg_model = PGModel.objects.filter(**params).first()
        if pg_model:
            [setattr(pg_model, k, v) for k, v in py_model.model_dump(exclude_none=False).items() if hasattr(pg_model, k)]
            pg_model.save()
        else:
            raise PGModel.DoesNotExist()
        # pg_author.save(**author)
        # postgres.Author(**author)
        # updated = postgres.Author.objects.filter(**params).update(**author)
    except PGModel.DoesNotExist as e:
        py_model.created_by = user
        pg_model, created  =   PGModel.objects.update_or_create(
                                    **params,
                                    defaults=py_model.model_dump(),
                                )
    return result

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
        # make models
        author = {}
        for key, value in data.items():
            if "date" in key:
                value = datetime.strptime(value, "%B %d, %Y").date()
            author[key] = value
        author["modified_by"] = admin

        py_author = Author.model_validate(author)

        uniques = [f for f in postgres.Author._meta.fields if f.unique]
        params = {u.name: author[u.name] for u in uniques if u.name in author}

        try:
            created = 0
            pg_author = postgres.Author.objects.filter(**params).first()
            if pg_author:
                [setattr(pg_author, k, v) for k, v in py_author.model_dump(exclude_none=False).items() if hasattr(pg_author, k)]
                pg_author.save()
            else:
                raise postgres.Author.DoesNotExist()
            # pg_author.save(**author)
            # postgres.Author(**author)
            # updated = postgres.Author.objects.filter(**params).update(**author)
        except postgres.Author.DoesNotExist as e:
            py_author.created_by = admin
            pg_author, created  =   postgres.Author.objects.update_or_create(
                                        **params,
                                        defaults=py_author.model_dump(),
                                    )
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
        # quote.update(py_logger)

        py_quote = Quote.model_validate(quote)

        uniques = [f for f in postgres.Quote._meta.fields if f.unique]
        params = {u.name: quote[u.name] for u in uniques if u.name in quote}

        try:
            created = 0
            pg_quote = postgres.Quote.objects.filter(**params).first()
            if pg_quote:
                [setattr(pg_quote, k, v) for k, v in py_quote.model_dump(exclude_none=False).items() if hasattr(pg_quote, k)]
                pg_quote.save()
            else:
                raise postgres.Quote.DoesNotExist()
            # quote = py_quote.model_dump()
            # quote = {k: v for k, v in quote.items() if v is not None}
            # updated = postgres.Quote.objects.filter(**params).update(**quote)
        except postgres.Quote.DoesNotExist as e:
            py_quote.created_by = admin
            pg_quote, created  =   postgres.Quote.objects.update_or_create(
                                        **params,
                                        defaults=py_quote.model_dump(),
                                    )
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
            # tag.update(py_logger)
            py_tag = Tag.model_validate(tag)

            uniques = [f for f in postgres.Tag._meta.fields if f.unique]
            params = {u.name: tag[u.name] for u in uniques if u.name in tag}
            
            try:
                created = 0
                pg_tag = postgres.Tag.objects.filter(**params).first()
                if pg_tag:
                    [setattr(pg_tag, k, v) for k, v in py_tag.model_dump(exclude_none=False).items() if hasattr(pg_tag, k)]
                    pg_tag.save()
                else:
                    raise postgres.Quote.DoesNotExist()
                # tag = py_tag.model_dump()
                # tag = {k: v for k, v in tag.items() if v is not None}
                # updated = postgres.Tag.objects.filter(**params).update(**tag)
            except postgres.Tag.DoesNotExist as e:
                py_tag.created_by = admin
                pg_tag, created =   postgres.Tag.objects.update_or_create(
                                            **params,
                                            defaults=py_tag.model_dump(),
                                    )
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
