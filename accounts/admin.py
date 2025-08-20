from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = [
        'id', 'username', 'name', 'email', 'phone',
        'is_staff', 'is_active', 'is_superuser',
        'date_joined', 'last_login'
    ]
    search_fields = ['username', 'name', 'email', 'phone']
    list_filter = ['is_staff', 'is_active', 'is_superuser', 'date_joined', 'last_login']
    ordering = ['-date_joined', '-last_login']

admin.site.register(CustomUser, CustomUserAdmin)