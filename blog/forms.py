from django import forms
from . import models


class PostsForm(forms.ModelForm):
    class Meta:
        model = models.Posts
        fields = ['title', 'content', 'language', 'link', 'image']


class LanguageForm(forms.ModelForm):
    class Meta:
        model = models.Posts
        fields = ['language']


class SearchForm(forms.Form):
    query = forms.CharField(max_length=250)


