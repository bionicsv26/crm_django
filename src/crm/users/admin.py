from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    """Класс для отображения пользователей в админке."""

    model = CustomUser
    list_display = ('full_name', 'is_staff', 'is_active',)
    list_filter = ('full_name', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('full_name', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('full_name', 'password1', 'password2', 'is_staff',
                       'is_active', "groups", "user_permissions"
                       )}),
    )
    search_fields = ('full_name',)
    ordering = ('full_name',)


admin.site.register(CustomUser, CustomUserAdmin)
