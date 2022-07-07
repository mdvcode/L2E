from django.urls import path

from . import views

app_name = 'message'

urlpatterns = [
    path('create_message/', views.create_message, name='create_message'),
    path('my_messages/', views.my_messages, name='my_messages'),
    path('info_message/<int:message_id>/', views.info_message, name='info_message'),
    ]
