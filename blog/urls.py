from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('lang/<int:language_id>/', views.lang, name='lang'),
    path('text/<int:id>/', views.text, name='text'),
    path('items_aut/<int:author_id>/', views.items_aut, name='items_aut'),
    path('add_lang/', views.add_lang, name='add_lang'),
    path('add_post/', views.add_post, name='add_post'),
    path('update_post/<int:post_id>/', views.update_post, name='update_post'),
    path('get/list/all/posts/', views.GetListAllPost.as_view()),
    path('get/list/all/languages/', views.GetListAllLanguages.as_view()),
    path('get/list/items/post/<int:id>/', views.ItemsPost.as_view()),
    path('create/post/', views.CreatePost.as_view()),
    path('update/post/<int:id>/', views.UpdatePost.as_view()),
    path('delete/post/<int:id>/', views.DeletePost.as_view()),
    path('get/list/post/to/user/<int:id>/<str:language>/', views.GetListPostToUser.as_view()),
    path('get/list/post/user/to/token/', views.GetListPostUserToToken.as_view()),
    path('get/privat/bank/', views.GetPrivatBank.as_view()),

]
