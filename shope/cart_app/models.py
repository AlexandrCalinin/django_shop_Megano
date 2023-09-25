from django.db import models

from core.models import BaseModelItem
from core.models.base_model import BaseModel
from auth_app.models import User
from django.utils.translation import gettext_lazy as _


class Cart(BaseModel):
    """
    Модель корзины пользователя.
    """

    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             verbose_name=_('user'),
                             related_name='carts')

    class Meta:
        verbose_name = _('Cart')

    def __str__(self):
        return f'{self.pk}-{self.user} - active({self.is_active})'


class CartItem(BaseModelItem):
    """
    Модель для хранения товаров в корзине.
    """

    cart_id = models.ForeignKey(Cart,
                                on_delete=models.CASCADE,
                                verbose_name=_('cart'),
                                related_name='cartitems')

    class Meta:
        verbose_name = _('CartItem')

    def __str__(self):
        return f'{self.cart_id} - {self.product}'
