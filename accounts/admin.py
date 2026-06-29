from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'display_name', 'account_type', 'is_staff', 'is_active')
    list_filter = ('account_type', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'display_name', 'first_name', 'last_name')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Información adicional', {'fields': ('display_name', 'account_type')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Información adicional', {'fields': ('display_name', 'account_type', 'email')}),
    )
