from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector
from django.contrib.sites.models import Site
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect

from .models import Posts
from .forms import PostsForm, LanguageForm, SearchForm


def search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Posts.objects.annotate(search=SearchVector('title', 'language', 'author').filter(search=query))
    return render(request, 'blog/search.html', context={'form': form, 'query': query, 'results': results})


def home(request):
    current_site = Site.objects.get_current()
    posts = Posts.objects.all()
    return render(request, 'blog/content.html', context={'posts': posts, 'domain': current_site.domain})


def lang(request, language):
    post = Posts.objects.filter(language=language)
    languages = ', '.join([language.name for language in post.language.all()])
    return render(request, 'blog/language.html', context={'post': post, 'languages': languages})


def text(request, id):
    current_site = Site.objects.get_current()
    posts = Posts.objects.get(pk=id)
    return render(request, 'blog/text.html', context={'posts': posts, 'domain': current_site.domain})


def items_aut(request, author):
    post = Posts.objects.filter(author=author)
    return render(request, 'blog/items_aut.html', context={'post': post})


@login_required(login_url='admin')
def add_lang(request: WSGIRequest):
    if request.method == 'POST':
        form = LanguageForm(request.POST, request.FILES)
        if form.is_valid():
            new_lang = form.save(commit=False)
            new_lang.save()
            return redirect('blog:home')
    form = LanguageForm()
    return render(request, 'blog/add_lang.html', context={'form': form})


@login_required(login_url='users:login')
# def add_post(request):
#     if request.method == 'POST':
#         form = PostsForm(request.POST, request.FILES)
#         if form.is_valid():
#             print('start')
#             new_post = form.save()
#             new_post.author = request.user
#             new_post.save()
#             print(new_post.author)
#             print('save')
#             return redirect('blog:home')
#     else:
#         form = PostsForm()
#     return render(request, 'blog/add_posts.html', context={'form': form})

def add_post(request):
    comment_form = PostsForm
    if request.method == "POST":
        comment_form = PostsForm(request.POST, request.FILES)
        if comment_form.is_valid():
            print('start')
            inst = comment_form.save(commit=False)
            inst.author = request.user
            inst.save()
            return redirect('blog:home')
    context = {
        'form': comment_form,
    }
    return render(request, 'blog/add_posts.html', context)
