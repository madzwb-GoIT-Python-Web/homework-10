from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.views import View
from django.contrib.auth.models import User

from .forms import AuthorForm, QuoteForm, TagForm
from .models import Author, Tag, Quote

# Create your views here.
def main(request, page=1):
    quotes = (
        Quote.objects.select_related("author")
        .prefetch_related("tags")
        .all()
        .order_by("created_at")
    )
    per_page = 10
    paginator = Paginator(quotes, per_page)
    quotes_on_page = paginator.page(page)
    return render(request, "quotes/index.html", context={"quotes": quotes_on_page})

def about(request, author_id):
    description = Author.objects.filter(pk=author_id)
    return render(request, "quotes/description.html", context={"authors": description})

def authors_by_tags(request, tag_name):
    tags = Tag.objects.filter(name=tag_name).first()
    quotes = tags.quote_set.all()
    return render(request, "quotes/tags.html", context={"quotes": quotes})


class AuthorView(View):

    template_name = "quotes/add_author.html"
    form_class = AuthorForm
    model = Author

    def get(self, request):
        return render(request, self.template_name, {"form": self.form_class()})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.created_by  = request.user
            instance.modified_by = request.user
            form.save()
            return redirect(to="quotes:main")

        return render(request, self.template_name, {"form": form})


class QuoteView(View):
    template_name = "quotes/add_quote.html"
    form_class = QuoteForm
    model = Quote

    def get(self, request):
        return render(request, self.template_name, {"form": self.form_class()})

    def post(self, request):

        form = self.form_class(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.created_by  = request.user
            instance.modified_by = request.user
            form.save()
            return redirect(to="quotes:main")

        return render(request, self.template_name, {"form": form})

class TagView(View):
    template_name = "quotes/add_tag.html"
    form_class = TagForm
    model = Tag

    def get(self, request):
        return render(request, self.template_name, {"form": self.form_class()})

    def post(self, request):

        form = self.form_class(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.created_by  = request.user
            instance.modified_by = request.user
            form.save()
            return redirect(to="quotes:main")

        return render(request, self.template_name, {"form": form})
