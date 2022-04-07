from django.contrib import admin

from blog.models import Posts, Language, IndexInfo, Kurs


class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'title', 'visible']


class KursAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'sale', 'buy', 'datetime']


admin.site.register(Posts, PostAdmin)
admin.site.register(Language)
admin.site.register(IndexInfo)
admin.site.register(Kurs, KursAdmin)


