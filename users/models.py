from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    username = models.CharField(max_length=250)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=250)
    password2 = models.CharField(max_length=250)

    def __str__(self):
        return self.username

