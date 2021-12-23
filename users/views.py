from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.template.response import TemplateResponse
from django.shortcuts import render, get_object_or_404

from users.forms import RegisterForm


# def signup(request):
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('users:login')
#     else:
#         form = RegisterForm()
#     return render(request, 'users/signup.html', context={'form': form})


def signup(request):
    if request.POST:
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:login')
    else:
        form = RegisterForm()
    return render(request, 'users/signup.html', {'form': form})


# def login(request):
#     if request.method == 'POST':
#         form = LoginForm(request=request, data=request.POST)
#         print(form)
#         print(form.get_user())
#         print('end')
#         if form is not None:
#             auth_login(request, form.get_user())
#             return redirect('blog:home')
#     else:
#         print('ERROR')
#         form = LoginForm()
#     return render(request, 'users/login.html', context={'form': form})


def logout(request):
    auth_logout(request)
    return redirect('users:login')


# def login(request, template="users/login.html", form_class=LoginForm, extra_context=None):
#     form = form_class(request.POST or None)
#     print(form)
#     if request.method == "POST" and form.is_valid():
#         authenticated_user = form.save()
#         print('start')
#         auth_login(request, authenticated_user)
#         print('end')
#         return redirect('blog:home')
#     context = {"form": form}
#     context.update(extra_context or {})
#     return TemplateResponse(request, template, context)

def login(request):
    logout(request)
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                from django.contrib.auth import login
                login(request, user)
                return redirect('/blog/home')
    context = {
        'form': AuthenticationForm(),
    }
    return render(request, 'users/login.html', context=context)
