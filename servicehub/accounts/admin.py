from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    # Show role & phone in the user list table
    list_display = ('username', 'email', 'role', 'phone', 'is_staff')

    # Add a filter sidebar to filter by role
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')

    # Add role & phone to the user edit form
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Info', {'fields': ('role', 'phone')}),
    )

    # Add role & phone to the "Add user" form
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Extra Info', {'fields': ('role', 'phone')}),
    )

admin.site.register(User, CustomUserAdmin)
