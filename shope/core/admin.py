"""Core admin."""


from django.contrib import admin
from .models import Seller


class SellerAdmin(admin.ModelAdmin):
    """Seller admin"""
    pass


admin.site.register(Seller, SellerAdmin)
