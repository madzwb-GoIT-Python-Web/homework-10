from django.forms import (
    ModelForm,
    CharField,
    TextInput,
    ModelChoiceField,
    ModelMultipleChoiceField,
    CheckboxSelectMultiple,
)
from .models import Tag, Author, Quote


class TagForm(ModelForm):

    class Meta:
        model = Tag
        fields = ["name"]


class QuoteForm(ModelForm):
    author = ModelChoiceField(queryset=Author.objects.all())
    tags = ModelMultipleChoiceField(
        queryset=Tag.objects.all().order_by("name"), widget=CheckboxSelectMultiple
    )

    class Meta:
        model = Quote
        fields = ["quote", "author", "tags"]


class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = ["fullname", "born_date", "born_location", "description"]
