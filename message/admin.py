from django.contrib import admin

from message.models import Message


class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'metamask', 'metamask_to', 'text', 'res_hash']


admin.site.register(Message, MessageAdmin)
