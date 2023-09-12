from django.core.validators import FileExtensionValidator
from django.db import models
from taggit.managers import TaggableManager

from auth_app.models import User
from core.models.base_discount import DiscountBaseModel
from core.models.base_model import BaseModel
from django.utils.translation import gettext_lazy as _


class Category(BaseModel):
    """Модель категории"""
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    image = models.FileField(
        upload_to="images/%Y/%m/%d", validators=[FileExtensionValidator(['svg'])], verbose_name=_('Image')
    )

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['id']


class Image(BaseModel):
    """Модель изображения для товара"""
    image = models.ImageField(upload_to="images/%Y/%m/%d", verbose_name=_('Image'))

    def __str__(self):
        return f'{self.image}'

    class Meta:
        verbose_name = _('Image')
        verbose_name_plural = _('Images')
        ordering = ['id']


class Product(BaseModel):
    """Модель товара"""
    title = models.CharField(max_length=255, verbose_name=_('Title  '))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    image = models.ManyToManyField('Image', related_name='image_to_product', verbose_name=_('Image'))
    tag = TaggableManager()
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name=_('Category'))
    is_limited = models.BooleanField(default=True, verbose_name=_('Limited'))
    is_delivery = models.BooleanField(default=True, verbose_name=_('Delivery'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        ordering = ['id']


class Slider(BaseModel):
    """Модель слайдера. Используется для набора сменяемых баннеров"""
    product = models.ForeignKey(
        'Product', on_delete=models.CASCADE, verbose_name=_('Product')
    )
    description = models.TextField(blank=True, verbose_name=_('Description'))
    image = models.ImageField(upload_to="images/%Y/%m/%d", verbose_name=_('Image'))

    def __str__(self):
        return self.product

    class Meta:
        verbose_name = _('Slider')
        verbose_name_plural = _('Sliders')
        ordering = ['id']


class Banner(BaseModel):
    """Модель баннера. Используется для сета баннеров с минимальными ценами в своей категории"""
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name=_('Category'))
    image = models.ImageField(upload_to="images/%Y/%m/%d", verbose_name=_('Image'))
    category_min_price = models.PositiveIntegerField(default=1, verbose_name=_('Minimal price'))

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = _('Slider')
        verbose_name_plural = _('Sliders')
        ordering = ['id']


class DiscountProduct(DiscountBaseModel):
    """Модель скидки на товар"""
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name=_('Product'))
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name=_('Category'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Product discount')
        verbose_name_plural = _('Product discounts')
        ordering = ['id']


class DiscountProductGroup(DiscountBaseModel):
    """Модель скидки на группу товаров"""
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name=_('Product'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Group of product discount')
        verbose_name_plural = _('Group of product discounts')
        ordering = ['id']


class CartSale(DiscountBaseModel):
    """Модель скидки на корзину"""
    amount = models.DecimalField(
        decimal_places=0, max_digits=7, verbose_name=_('Amount of products for a success discount')
    )
    quantity = models.PositiveIntegerField(default=2, verbose_name=_('Quantity of products for a success discount'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Cart discount')
        verbose_name_plural = _('Cart discounts')
        ordering = ['id']


class Rewiew(BaseModel):
    """Модель отзывов"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Rewiew'))
    text = models.CharField(max_length=255, verbose_name=_('Text'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('Product'))

    def __str__(self):
        return self.user

    class Meta:
        verbose_name = _('Rewiew')
        verbose_name_plural = _('Reviews')


###############################################################
# ХАРАКТЕРИСТИКИ ПРОДУКТОВ
###############################################################

class CharacteristicType(BaseModel):
    """Виды характеристик продуктов"""

    name = models.CharField(verbose_name=_('name'),
                            max_length=150
                            )

    category = models.ForeignKey('Category',
                                 on_delete=models.CASCADE,
                                 verbose_name=_('category'),
                                 )

    class Meta:
        """Meta"""
        verbose_name = _('type characteristic of product')
        verbose_name_plural = _('types characteristic of product')

    def __str__(self):
        """Строковое представление"""
        return str(self.name)


class CharacteristicValue(BaseModel):
    """Значение характеристики продукта"""
    characteristic_type = models.ForeignKey(CharacteristicType,
                                            on_delete=models.CASCADE,
                                            verbose_name=_('type of characteristic'),
                                            related_name='characteristic_value'
                                            )
    value = models.CharField(verbose_name=_('value'),
                             max_length=100
                             )

    class Meta:
        """Meta"""
        verbose_name = _('characteristic value')
        verbose_name_plural = _('characteristic values')

    def __str__(self):
        """Строковое представление"""
        return f'{self.characteristic_type} - {self.value}'


class CharacteristicProduct(BaseModel):
    """Значение характеристики в продукте"""
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                verbose_name=_('product'),
                                related_name='characteristic_product'
                                )

    characteristic_value = models.ForeignKey(CharacteristicValue,
                                             on_delete=models.CASCADE,
                                             verbose_name=_('value of characteristic'),
                                             related_name='characteristic_product'
                                             )

    class Meta:
        """Meta"""
        verbose_name = _('characteristic of product')
        verbose_name_plural = _('characteristics of product')

    def __str__(self):
        """Строковое представление"""
        return f'{self.product} - {self.characteristic_value}'
