from django.db import models
from .base_model import BaseModel
from core.models.seller import Seller
from catalog_app.models import Product
from django.utils.translation import gettext_lazy as _


class Price(BaseModel):
    """Модель цены товара"""
    price = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name=_("Product's price"))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('Product'))
    seller = models.ForeignKey(
        Seller, on_delete=models.CASCADE, related_name="product_seller", verbose_name=_('Seller')
    )

    def __str__(self):
        return str(self.price)

    class Meta:
        verbose_name = _('Price')
        verbose_name_plural = _('Prices')
        ordering = ['id']
