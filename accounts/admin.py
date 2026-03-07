from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('address', 'profile_image', 'role', 'is_email_verified')}),
    )
    list_display = ['email', 'first_name', 'last_name', 'role', 'is_email_verified', 'created_at']
    search_fields = ['email', 'first_name', 'last_name']
    list_filter = ['role', 'is_email_verified', 'created_at']
