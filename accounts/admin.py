from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account

# Register your models here.

@admin.register(Account)
class AccountAdmin(UserAdmin):
    list_display = [
        'email', 'username', 'first_name', 'last_name', 'date_joined', 'last_login', 'is_active'
    ]

    list_display_links = [
        'first_name', 'email', 'username'
    ]

    readonly_fields = ('date_joined', 'last_login',)
    ordering = ('-date_joined',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
