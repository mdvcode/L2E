import email

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.shortcuts import render, redirect


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:login')
    form = UserCreationForm()
    return render(request, 'users/signup.html', context={'form': form})


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('blog:home')
    form = AuthenticationForm()
    return render(request, 'users/login.html', context={'form': form})


def logout(request):
    auth_logout(request)
    return redirect('users:login')



