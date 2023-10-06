from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.forms import CharField, TextInput, EmailField, EmailInput, PasswordInput


class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    
    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )


class LoginForm(AuthenticationForm):
    username = CharField(max_length=100, required=True, widget=TextInput(attrs={"class": "form-control"}), )
    password = CharField(max_length=20, min_length=4, required=True, widget=PasswordInput(attrs={"class": "form-control"}), )

    class Meta:
        model = User
        fields = ("username", "password")
