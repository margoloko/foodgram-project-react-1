from django.contrib import admin
from django.contrib.admin import register

from .models import User, Follow


@register(User)
class PersonAdmin(admin.ModelAdmin):
    list_display = (
        'username', 'first_name', 'last_name', 'email',)
    exclude = ('password',)
    list_filter = ('first_name', 'email',)
    save_on_top = True


@register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'user',
    )
    search_fields = ('user', 'author',)
    list_per_page = 20
    save_on_top = True