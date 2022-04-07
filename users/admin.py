from django.contrib import admin

from users.models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone', 'telegram', 'instagram', 'photo', 'email', 'pin')


admin.site.register(Profile, ProfileAdmin)




