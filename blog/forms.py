from django import forms
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

from . import models
from .models import Posts, Language


class PostsForm(forms.ModelForm):
    class Meta:
        model = models.Posts
        fields = ['title', 'content', 'language', 'link', 'image']


class LanguageForm(forms.ModelForm):
    class Meta:
        model = models.Language
        fields = ['name']


class SearchForm(forms.Form):
    query = forms.CharField(max_length=250)


class UpdatePostsForm(forms.ModelForm):
    class Meta:
        model = models.Posts
        fields = ['title', 'slug', 'image', 'language', 'content', 'link']


class FilterPostForm(forms.Form):
    language = forms.ModelMultipleChoiceField(
        queryset=Language.objects.all()
    )
    author = forms.ModelMultipleChoiceField(
        queryset=User.objects.all()
    )



