from django.db import models
from shope.core.models import BaseModel


class BaseModelItem(BaseModel):

    """
    Базовая модель для корзины и заказов.
    """

    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='Товар')
    seller = models.ForeignKey('Seller', on_delete=models.CASCADE, verbose_name='Продавец')
    count = models.IntegerField(verbose_name='Кол-во товаров')
    amount = models.DecimalField(verbose_name='Сумма')


class Cart(BaseModel):

    """
    Модель корзины пользователя.
    """

    user = models.OneToOneField('User', on_delete=models.CASCADE, verbose_name='Пользователь')

    class Meta:
        verbose_name = 'Корзина'


class CartItem(BaseModelItem):

    """
    Модель для хранения товаров в корзине.
    """

    cart_id = models.ForeignKey('Cart', on_delete=models.CASCADE, verbose_name='Корзина')

