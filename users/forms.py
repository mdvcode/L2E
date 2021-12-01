from django import forms
from django.contrib.auth.forms import UserCreationForm

from . import models
from .models import Author


class RegisterForm(UserCreationForm):
    email = forms.EmailField(unique=True)

    class Register:
        model = Author
        fields = ['username', 'email', 'password', 'password2']
