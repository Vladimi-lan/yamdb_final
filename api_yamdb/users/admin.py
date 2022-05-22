from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class CustomUserAdmin(UserAdmin):
    list_display = (
        'username', 'email', 'first_name',
        'last_name', 'bio', 'role', 'date_joined',
        'is_active', 'is_staff', 'is_superuser',
        'is_moderator', 'is_admin', 'is_user')
    fieldsets = ()
    search_fields = ('username',)
    list_filter = ('role',)
    empty_value_display = '-пусто-'


admin.site.register(User, CustomUserAdmin)
