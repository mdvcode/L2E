from django.urls import path
from . import views

app_name = 'w3'

urlpatterns = [
    path('connect/', views.connect, name='connect'),
    path('create_trans/<int:id_acc>/', views.create_trans, name='create_trans'),
    path('create_text_trans/<int:id_acc>/', views.create_text_trans, name='create_text_trans'),
    path('redaction/<int:id>/', views.redaction, name='redaction'),

]