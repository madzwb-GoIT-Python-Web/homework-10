from django.db import models
# from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User

# Create your models here.
class Logger(models.Model):
      created_by    = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
      modified_by   = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
      created_at    = models.DateTimeField(null=False, auto_now_add =True)
      modified_at   = models.DateTimeField(null=False, auto_now     =True)

class Author(Logger):
    fullname        = models.CharField(max_length=128, null=False, unique=True)
    born_date       = models.DateTimeField(null=False,)
    born_location   = models.CharField(max_length=128, null=False, unique=True)
    description     = models.CharField(max_length=1024, null=False, unique=True)

    def __str__(self):
            return f"{self.fullname}"

class Tag(Logger):
    name = models.CharField(max_length=32, null=False, unique=True)
    
    def __str__(self):
            return f"{self.name}"

class Quote(Logger):
    quote   = models.CharField(max_length=1024, null=False, unique=True)
    # tags    = ArrayField(models.CharField(max_length=256, null=False, unique=True))
    tags = models.ManyToManyField(Tag)

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    def __str__(self):
            return f"{self.quote}"


# class Tags(models.Model):
#     tag     = models.ForeignKey(Tag     , on_delete=models.CASCADE)
#     quote   = models.ForeignKey(Quote   , on_delete=models.CASCADE)
#     # name = models.CharField(max_length=32, null=False, unique=True)
#     pass

