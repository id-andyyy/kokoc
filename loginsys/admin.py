from django.contrib import admin
from .models import Profiles


class ProfilesAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'points')
    list_display_links = ('id', 'user')
    list_filter = ('role',)


admin.site.register(Profiles, ProfilesAdmin)
