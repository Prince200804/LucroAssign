from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, AnonymousSession


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'username', 'first_name', 'last_name', 'is_admin', 'is_active', 'created_at']
    list_filter = ['is_admin', 'is_active', 'created_at']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    ordering = ['-created_at']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone', 'address', 'city', 'state', 'zip_code', 'country', 'is_admin')}),
    )


@admin.register(AnonymousSession)
class AnonymousSessionAdmin(admin.ModelAdmin):
    list_display = ['session_key', 'ip_address', 'created_at', 'last_activity']
    search_fields = ['session_key', 'ip_address']
    ordering = ['-last_activity']
