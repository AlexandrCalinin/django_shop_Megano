"""Core admin."""


from django.contrib import admin
from .models import Seller, Price


class SellerAdmin(admin.ModelAdmin):
    """Seller admin"""
    pass


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Price._meta.fields]


admin.site.register(Seller, SellerAdmin)
