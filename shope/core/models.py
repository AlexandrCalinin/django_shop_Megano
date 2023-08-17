"""Общие модели проекта."""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from shope.catalog_app.models import Product


class BaseModel(models.Model):
    """Модель Базовая"""
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation time'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated time'))
    is_active = models.BooleanField(default=True, verbose_name=_('Active'))

    class Meta:
        abstract = True


class Seller(BaseModel):
    """Модель продавцов товаров"""
    name = models.CharField(verbose_name=_('name'),
                            max_length=120)

    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                verbose_name=_('user'),
                                related_name='seller',
                                )

    class Meta:
        """Meta class"""
        verbose_name = _('seller')
        verbose_name_plural = _('sellers')

    def __str__(self) -> str:
        """Строкое представление."""
        return self.name


class BaseModelItem(BaseModel):

    """
    Базовая модель для корзины и заказов.
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('product'))
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, verbose_name=_('seller'))
    count = models.IntegerField(verbose_name=_('count product'))
    amount = models.DecimalField(verbose_name=_('amount'))

    class Meta:
        abstract = True
