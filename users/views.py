import random
from django.contrib.auth import logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import redirect
from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from blog.models import IndexInfo, Language
from users.forms import RegisterForm, UpdateForm
from users.models import Profile
from users.serializer import ProfileSerializer, AuthorSerializer


def signup(request):
    if request.POST:
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:login')
    else:
        form = RegisterForm()
    return render(request, 'users/signup.html', {'form': form})


def logout(request):
    auth_logout(request)
    return redirect('users:login')


def login(request):
    logout(request)
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        print(username)
        print(password)
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


@login_required(login_url='users/login')
def profile(request):
    index = IndexInfo.objects.all()[0]
    languages = Language.objects.all()
    try:
        profile = Profile.objects.filter(user=request.user)[0]
    except:
        Profile.objects.create(user=request.user)
        profile = Profile.objects.filter(user=request.user)[0]
    current_site = Site.objects.get_current()
    if request.method == "POST":
        form = UpdateForm(instance=request.user.profile, files=request.FILES or None, data=request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('/users/profile')
    form = UpdateForm(instance=request.user.profile)
    return render(request, 'users/profile.html', context={'profile': profile, 'domain': current_site, 'index': index,
                                                          'languages': languages, 'form': form})


class GetListAllAuthor(generics.ListAPIView):
    serializer_class = AuthorSerializer

    def get_queryset(self):
        return User.objects.all()


class UpdateProfile(APIView):
    def get_object(self, id):
        try:
            return Profile.objects.get(id=id)
        except:
            raise Http404

    def patch(self, request, id, *args, **kwargs):
        item = self.get_object(id)
        serializer = ProfileSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class GetUsernameToToken(APIView):
    def post(self, request, *args, **kwargs):
        return Response(request.user.username)


class GetProfileToToken(APIView):
    def get_object(self, user):
        try:
            return Profile.objects.get(user=user)
        except:
            raise Http404

    def get(self, request, *args, **kwargs):
        object = self.get_object(request.user)
        serializer = ProfileSerializer(object)
        return Response(serializer.data)


class SentMailUser(APIView):
    def post(self, request, *args, **kwargs):
        try:
            message = request.data.get('message')
            to_email = request.data.get('to_email')
            subject = request.data.get('subject')
            if message != None and subject != None and to_email != None:
                send_mail(
                    subject,
                    message,
                    'mard9378@gmail.com',
                    [to_email],
                    fail_silently=False,
                )
                return Response('Send email!')
            else:
                return Response('invalid data!')
        except:
            return Response('error connection')


class SendRecetPin(APIView):
    def post(self, request, *args, **kwargs):
        try:
            email = request.data.get('email')
            if email != None:
                pin = ''.join([str(random.randint(0, 10)) for _ in range(4)])
                Profile.objects.filter(email=email).update(pin=pin)
                send_mail(
                    'recet password',
                    'you recet pin:' + str(pin),
                    'mard9378@gmail.com',
                    [email],
                    fail_silently=False,
                )
                return Response('Send email')
            else:
                return Response('no valid email')
        except:
            return Response('error connection')


class RecetPassword(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        pin = request.data.get('pin')
        if email != None and pin != None:
            profile = Profile.objects.filter(email=email, pin=pin)[0]
            print(profile)
            u = User.objects.get(username=profile.user.username)
            u.set_password('new password')
            u.save()
        return Response('Hello')
