from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import Posts
from .forms import PostsForm


def home(request):
    posts = Posts.objects.all()
    return render(request, 'blog/content.html', context={'post': posts})


def lang(request, language):
    post = Posts.objects.get(language=language)
    languages = ', '.join([language.name for language in post.language.all()])
    return render(request, 'blog/language.html', context={'posts': post, 'languages': languages})


def text(request, id):
    posts = Posts.objects.get(pk=id)
    return render(request, 'blog/text.html', context={'post': posts})


def items_aut(request, author):
    post = Posts.objects.filter(author=author)
    return render(request, 'blog/items_aut.html', context={'posts': post})


@login_required(login_url='users:login')
def add_post(request):
    if request.method == 'POST':
        form = PostsForm(request.Post)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return redirect('blog:home')
    form = PostsForm()
    return render(request, 'blog/add_posts.html', context={'form': form})



