"""User admin."""


from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    """User admin"""
    pass


admin.site.register(User, UserAdmin)
