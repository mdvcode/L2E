import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.postgres.search import SearchQuery, SearchVector
from django.contrib.sites.models import Site
from django.core.handlers.wsgi import WSGIRequest
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from web3 import Web3, HTTPProvider

from .models import Posts, Language, IndexInfo, Bitcoin
from .forms import PostsForm, LanguageForm, SearchForm, UpdatePostsForm, FilterPostForm
from .pagination import PostsPagination
from .serializers import PostsSerializer, LanguagesSerializer, PostCreateSerializer


def home(request):
    index = IndexInfo.objects.all()[0]
    current_site = Site.objects.get_current()
    authors = User.objects.all()
    posts = Posts.objects.all()
    paginator = Paginator(posts, 10)
    page_num = request.GET.get('page')
    bit = Bitcoin.objects.all()
    w3 = Web3(HTTPProvider())
    try:
        posts = paginator.page(page_num)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    languages = Language.objects.all()
    form_filter = FilterPostForm
    if request.POST:
        form_filter = FilterPostForm(request.POST)
        if form_filter.is_valid():
            language = form_filter.cleaned_data.get('language')
            language_id = []
            author = form_filter.cleaned_data.get('author')
            author_id = []
            for item in author:
                author_id.append(item.id)
            for item in language:
                language_id.append(item.id)
            if len(language_id) > 0 and len(author_id) == 0:
                posts = Posts.objects.filter(language_id__in=language_id)
            if len(author_id) > 0 and len(language_id) == 0:
                posts = Posts.objects.filter(author_id__in=author_id)

            if len(author_id) > 0 and len(language_id) > 0:
                posts = Posts.objects.filter(author_id__in=author_id, language_id__in=language_id)
        else:
            form_filter = FilterPostForm

    form = SearchForm()
    if request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            posts = Posts.objects.annotate(search=SearchVector('title', 'author__username', 'language__name')).filter(
                search=query)
    return render(request, 'blog/content.html', context={'posts': posts, 'form': form,
                                                         'domain': current_site.domain, 'languages': languages,
                                                         'index': index, 'authors': authors,
                                                         'form_filter': form_filter, 'w3': w3, 'bit': bit})


def lang(request, language_id):
    index = IndexInfo.objects.all()[0]
    languages = Language.objects.all()
    posts = Posts.objects.filter(language_id=language_id)
    return render(request, 'blog/language.html', context={'posts': posts, 'index': index, 'languages': languages})


def text(request, id):
    index = IndexInfo.objects.all()[0]
    languages = Language.objects.all()
    current_site = Site.objects.get_current()
    post = Posts.objects.get(pk=id)
    return render(request, 'blog/text.html', context={'post': post, 'domain': current_site.domain, 'index': index,
                                                      'languages': languages})


def update_post(request, post_id):
    index = IndexInfo.objects.all()[0]
    languages = Language.objects.all()
    post = Posts.objects.get(id=post_id)
    if request.method == "POST":
        form = UpdatePostsForm(instance=post, files=request.FILES or None, data=request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('blog:text', id=post_id)
    form = UpdatePostsForm(instance=post)
    return render(request, 'blog/update_trans.html', context={'index': index, 'languages': languages, 'form': form})


def items_aut(request, author_id):
    index = IndexInfo.objects.all()[0]
    languages = Language.objects.all()
    posts = Posts.objects.filter(author_id=request.user.id)
    return render(request, 'blog/items_aut.html', context={'posts': posts, 'index': index, 'languages': languages})


@login_required(login_url='users/login')
def add_lang(request: WSGIRequest):
    index = IndexInfo.objects.all()[0]
    languages = Language.objects.all()
    if request.method == 'POST':
        form = LanguageForm(request.POST, request.FILES)
        if form.is_valid():
            new_lang = form.save(commit=False)
            new_lang.save()
            return redirect('blog:home')
    form = LanguageForm()
    return render(request, 'blog/add_lang.html', context={'form': form, 'index': index, 'languages': languages})


@login_required(login_url='users:login')
def add_post(request):
    comment_form = PostsForm
    index = IndexInfo.objects.all()[0]
    languages = Language.objects.all()
    if request.method == "POST":
        comment_form = PostsForm(request.POST, request.FILES)
        if comment_form.is_valid():
            inst = comment_form.save(commit=False)
            inst.author = request.user
            inst.save()
            return redirect('blog:home')
    context = {
        'form': comment_form, 'index': index, 'languages': languages
    }
    return render(request, 'blog/add_posts.html', context)


class GetListAllPost(generics.ListAPIView):
    serializer_class = PostsSerializer
    pagination_class = PostsPagination

    def get_queryset(self):
        return Posts.objects.filter(visible=True)


class GetListAllLanguages(generics.ListAPIView):
    serializer_class = LanguagesSerializer

    def get_queryset(self):
        return Language.objects.all()


class GetListPostToUser(generics.ListAPIView):
    serializer_class = PostsSerializer

    def get_queryset(self):
        id_user = self.kwargs['id']
        language_user = self.kwargs['language']
        return Posts.objects.filter(author_id=id_user, language=get_object_or_404(Language, name=language_user),
                                    visible=True)


class ItemsPost(APIView):
    def get_object(self, id):
        try:
            return Posts.objects.get(id=id)
        except:
            raise Http404

    def get(self, request, id, *args, **kwargs):
        object = self.get_object(id)
        serializer = PostsSerializer(object)
        return Response(serializer.data)


class CreatePost(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PostCreateSerializer(data=request.data)
        if serializer.is_valid():
            count_post = Posts.objects.filter(content=request.data.get('content'), title=request.data.get('title')).count()
            if count_post == 0:
                serializer.save(visible=False, author_id=request.user.id)
                return Response(serializer.data)
            else:
                return Response('content not unique, title not unique')
        return Response(serializer.errors)


class UpdatePost(APIView):
    def get_object(self, id):
        try:
            return Posts.objects.get(id=id)
        except:
            raise Http404

    def patch(self, request, id):
        item = self.get_object(id)
        if str(item.author) == str(request.user) or request.user.is_superuser:
            serializer = PostCreateSerializer(item, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(visible=False)
                return Response(serializer.data)
            return Response(serializer.errors)
        else:
            return Response({'message': 'No permission delete post!'})


class DeletePost(APIView):
    def get_object(self, id):
        try:
            return Posts.objects.get(id=id)
        except:
            raise Http404

    def delete(self, request, id, *args, **kwargs):
        item = self.get_object(id)
        if str(item.author) == str(request.user):
            item.delete()
            return Response({"message": 'Delete!'})
        else:
            return Response({"message": 'No permission delete post'})


class GetListPostUserToToken(generics.ListAPIView):
    serializer_class = PostsSerializer

    def get_queryset(self):
        return Posts.objects.filter(author_id=self.request.user.id)


class GetPrivatBank(APIView):
    def get(self, request, *args, **kwargs):
        bit = requests.get('https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5')
        result = bit.json()
        object_bit = Bitcoin.objects.all().order_by('-id')[0]
        if object_bit.sale != float(result[0].get('sale')) or object_bit.buy != float(result[0].get('buy')):
            new_bit = Bitcoin(name=result[0].get('base_ccy'), buy=result[0].get('buy'), sale=result[0].get('sale'))
            new_bit.save()
        return Response(result)
