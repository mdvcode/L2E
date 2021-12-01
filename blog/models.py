from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from users.models import Author


class Language(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Posts(models.Model):
    objects = None
    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True, allow_unicode=True, default=None, blank=True, null=True)
    image = models.ImageField(max_length=250)
    language = models.ManyToManyField(Language)
    content = models.TextField()
    link = models.URLField(max_length=1000)
    author = models.ManyToManyField(Author)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.language}: {self.datetime}'

    class Meta:
        ordering = ['datetime']

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(force_insert=False, force_update=False, using=None, update_fields=None)

    @property
    def url_slug(self):
        return '{}-{}'.format(self.slug, self.id)
