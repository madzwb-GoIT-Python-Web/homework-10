from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Author, Quote, Tag, Tags

# Register your models here.
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Quote)

# admin.site.register(Tags)
