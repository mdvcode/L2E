from django.contrib.auth.models import User
from rest_framework import serializers

from blog.models import Posts, Language


class LanguagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['name']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class PostsSerializer(serializers.ModelSerializer):
    language = LanguagesSerializer(read_only=True, many=False)
    author = UserSerializer(read_only=True, many=False)

    class Meta:
        model = Posts
        fields = '__all__'


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = '__all__'




