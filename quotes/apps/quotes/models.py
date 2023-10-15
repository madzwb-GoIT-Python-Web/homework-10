from typing import Any
from django.db import models
# from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from django.db.models import Model

# Create your models here.

class UserField(models.ForeignKey):

    # def clean(self, value: Any, model_instance: Model | None) -> Any:
    #      return super().clean(value, model_instance)
    
    def pre_save(self, model_instance, add):
        if add:
            value = getattr(model_instance, self.attname)
            if value is None:
                 value = 1 # User with pk=1 is "admin"
            return value
        else:
            value = getattr(model_instance, self.attname)
            if value is None:
                 model_instance.refresh_from_db(fields=[self.attname]) # Restore old value
            return super().pre_save(model_instance, add)
        
class Logger(models.Model):
    created_by    = UserField(User, to_field="id" , on_delete=models.CASCADE, null=False, related_name="%(app_label)s_%(class)s_created_by",)# default=User.objects.get(pk=1))
    modified_by   = UserField(User, to_field="id" , on_delete=models.CASCADE, null=False, related_name="%(app_label)s_%(class)s_modified_by",)# default=User.objects.get(pk=1))
    created_at    = models.DateTimeField(null=False, auto_now_add =True)
    modified_at   = models.DateTimeField(null=False, auto_now     =True)

    class Meta:
            abstract = True
    
class Author(Logger):
    fullname        = models.CharField(max_length=256, null=False, unique=True)
    born_date       = models.DateField(null=False,)
    born_location   = models.CharField(max_length=1024, null=False)
    description     = models.TextField(null=False)

    def __str__(self):
            return f"{self.fullname}"

class Tag(Logger):
    name = models.CharField(max_length=256, null=False, unique=True)
    
    def __str__(self):
            return f"{self.name}"

class Quote(Logger):
    quote   = models.TextField(null=False, unique=True)
    # tags    = ArrayField(models.CharField(max_length=256, null=False, unique=True))
    tags = models.ManyToManyField(Tag)

    author = models.ForeignKey(Author, on_delete=models.CASCADE)#, related_name="author_id")
    def __str__(self):
            return f"{self.quote}"


# class Tags(models.Model):
#     tag     = models.ForeignKey(Tag     , on_delete=models.CASCADE)
#     quote   = models.ForeignKey(Quote   , on_delete=models.CASCADE)
#     # name = models.CharField(max_length=32, null=False, unique=True)
#     pass

