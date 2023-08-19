from django.db import models

from core.models import BaseModelItem
from core.models.base_model import BaseModel
from auth_app.models import User
from django.utils.translation import gettext_lazy as _


class Cart(BaseModel):
    """
    Модель корзины пользователя.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('user'))

    class Meta:
        verbose_name = _('Cart')

    def __str__(self):
        return self.user


class CartItem(BaseModelItem):
    """
    Модель для хранения товаров в корзине.
    """

    cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name=_('cart'))

    class Meta:
        verbose_name = _('CartItem')

    def __str__(self):
        return self.cart_id