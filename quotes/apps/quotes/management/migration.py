from datetime import date
from pydantic import BaseModel, ConfigDict
from homework_8_1 import models as mongodb

from .. import models as postgres

class Logger(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

    created_by      : postgres.User|None = None
    modified_by     : postgres.User#|None = None



class Author(Logger):
    fullname        : str
    born_date       : date
    born_location   : str
    description     : str



class Quote(Logger):
    author      : postgres.Author|mongodb.Author|str|None = None
    quote       : str
    # tags        : list[str]



class Tag(Logger):
    name        : str



def update_or_create(data, PYModel, PGModel):

    py_model = PYModel.model_validate(data)

    uniques = [f for f in PGModel._meta.fields if f.unique]
    params = {u.name: data[u.name] for u in uniques if u.name in data}

    try:
        created = False
        pg_model = PGModel.objects.filter(**params).first()
        if pg_model:
            # Fill pg_model for saving.
            [
                setattr(pg_model, k, v)
                for k, v in py_model.model_dump(exclude_none=False).items()
                if hasattr(pg_model, k)
            ]
            pg_model.save()
        else:
            raise PGModel.DoesNotExist()
    except PGModel.DoesNotExist as e:
        py_model.created_by = py_model.modified_by
        pg_model, created  =   PGModel.objects.update_or_create(
                                    **params,
                                    defaults=py_model.model_dump(),
                                )
    return pg_model, created
