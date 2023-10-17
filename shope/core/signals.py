"""Signals for cache"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from core.utils.cache import delete_cache_setup

from core.models.cache_setup import CacheSetup
from catalog_app.models import Rewiew, Product, Category, Banner
from order_app.models import OrderItem
from .utils.cache import invalidate_cache


@receiver(post_save, sender=CacheSetup)
def cache_setup_change(sender, instance, **kwargs):
    """Изменение настроек кеша.
    Удаляем кеш настроек"""

    delete_cache_setup()


@receiver(post_save, sender=Rewiew)
def review_change(sender, instance, **kwargs):
    """ Создание отзыва.
    Удаляем кеш детальной страницы продукта на странице которого создан отзыв"""
    # invalidate_cache('product', instance.product_id)
    key = 'DETAIL_PRODUCT:' + str(instance.product_id)
    if cache.get(key):
        cache.delete(key)

    key = make_template_fragment_key('detail_product', (instance.product_id,))
    if key:
        cache.delete(key)


@receiver(post_save, sender=Product)
def product_change(sender, instance, **kwargs):
    """Изменение продукта.
    Удаляем кеш детальной страницы продукта на странице которого создан отзыв"""

    key = 'DETAIL_PRODUCT:' + str(instance.pk)
    if cache.get(key):
        cache.delete(key)

    key = make_template_fragment_key('detail_product', (instance.pk,))
    if key:
        cache.delete(key)


@receiver(post_save, sender=Category)
def category_change(sender, instance, **kwargs):
    """Изменение категории.
    Удаляем кеш категории из контекст-процессора"""

    key = 'CATEGORY_LIST'
    if cache.get(key):
        cache.delete(key)


@receiver(post_save, sender=Banner)
def banner_change(sender, instance, **kwargs):
    """Изменение  банера.
    Удаляем кеш банера"""

    key = 'BANNER_LIST'
    if cache.get(key):
        cache.delete(key)


@receiver(post_save, sender=OrderItem)
@receiver(post_save, sender=Product)
def top_product_change(sender, instance, **kwargs):
    """Отслеживаем изменениен продукта и изменение заказа.
    Удаляем кеш топ-товаров"""

    key = 'TOP_PRODUCT_LIST'
    if cache.get(key):
        cache.delete(key)
