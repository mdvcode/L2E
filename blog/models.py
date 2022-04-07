from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from datetime import datetime


class Language(models.Model):
    objects = None
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Posts(models.Model):
    objects = None
    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True, allow_unicode=True, default=None, blank=True, null=True)
    image = models.ImageField(max_length=250, blank=True, null=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    content = models.TextField()
    link = models.URLField(max_length=1000, blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    update_date = models.DateTimeField(default=datetime.now, null=True, blank=True)
    datetime = models.DateTimeField(auto_now_add=True)
    visible = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.title}: {self.language}: {self.datetime}'

    class Meta:
        ordering = ['datetime']

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)

    @property
    def url_slug(self):
        return '{}-{}'.format(self.slug, self.id)


@receiver(post_save, sender=Posts)
def create_user_profile(sender, instance, created, **kwargs):
    post = Posts.objects.filter(id=instance.id)
    new_date = datetime.now()
    post.update(update_date=new_date)


class IndexInfo(models.Model):
    objects = None
    phone = models.CharField(max_length=250)
    facebook = models.CharField(max_length=250)
    instagram = models.CharField(max_length=250)


class Kurs(models.Model):
    objects = None
    name = models.CharField(max_length=250)
    buy = models.FloatField(default=0)
    sale = models.FloatField(default=0)
    datetime = models.DateTimeField(auto_now_add=True)



