from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager

from core.models.base_model import BaseModel
from django.utils.translation import gettext_lazy as _


class Category(BaseModel):
    """Модель категории"""
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    image = models.ImageField(upload_to="images/%Y/%m/%d", verbose_name=_('Image'))

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['id']


class Image(BaseModel):
    """Модель изображения для товара"""
    image = models.ImageField(upload_to="images/%Y/%m/%d", verbose_name=_('Image'))
    product = models.ForeignKey(
        'Product', on_delete=models.CASCADE, related_name='image_for_product', verbose_name=_('Product')
    )

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

    def _tag(self):
        return [t.name for t in self.tag.all()]
