from django.urls import path
from django.views.generic import CreateView

from . import views
from .views import GetUsernameToToken, GetProfileToToken, GetListAllAuthor, SentMailUser, SendRecetPin, RecetPassword

app_name = 'users'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('get/username/to/token/', GetUsernameToToken.as_view()),
    path('get/list/all/author/', GetListAllAuthor.as_view()),
    path('get/profile/to/token/', GetProfileToToken.as_view()),
    path('send/mail/to/user/', SentMailUser.as_view()),
    path('send/recet/pin/', SendRecetPin.as_view()),
    path('send/recet/password/', RecetPassword.as_view()),
]
