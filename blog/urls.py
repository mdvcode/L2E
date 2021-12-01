from django.contrib import admin
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('lang/<str:language>/', views.lang, name='lang'),
    path('text/<int:id>/', views.text, name='text'),
    path('items_aut/<str:author>/', views.items_aut, name='items_aut'),
    path('add_post/', views.add_post, name='add_post'),

]
