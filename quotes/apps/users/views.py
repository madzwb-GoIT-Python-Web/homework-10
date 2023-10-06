from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.edit import FormView
from django.contrib import messages  # зберігає до першого зчитування дані

from .forms import RegisterForm

from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = "users/signup.html"

    def get(self, request):
        return render(request, self.template_name, {"form": self.form_class()})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            messages.success(request, f"{username}, your account has been successfully created!")
            return redirect(to="users:signin")

        return render(request, self.template_name, {"form": form})
