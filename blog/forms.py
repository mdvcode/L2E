from django import forms
from . import models


class PostsForm(forms.ModelForm):
    class Post:
        model = models.Posts
        fields = ['title', 'content', 'language', 'link', 'image']
