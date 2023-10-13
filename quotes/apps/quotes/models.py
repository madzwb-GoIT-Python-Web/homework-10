from django.db import models
# from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User

# Create your models here.
class Logger(models.Model):
    created_by    = models.ForeignKey(User, to_field="id" , on_delete=models.CASCADE, null=False, related_name="%(app_label)s_%(class)s_created_by",)# default=User.objects.get(pk=1))
    modified_by   = models.ForeignKey(User, to_field="id" , on_delete=models.CASCADE, null=False, related_name="%(app_label)s_%(class)s_modified_by",)# default=User.objects.get(pk=1))
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

