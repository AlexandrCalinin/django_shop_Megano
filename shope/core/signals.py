"""Signals for cache"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key


from catalog_app.models import Rewiew
from catalog_app.models import Product
from .utils.cache import invalidate_cache


@receiver(post_save, sender=Rewiew)
def rewiew_change(sender, instance, **kwargs):
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
    # invalidate_cache('product', instance.product_id)
    key = 'DETAIL_PRODUCT:' + str(instance.pk)
    if cache.get(key):
        cache.delete(key)

    key = make_template_fragment_key('detail_product', (instance.pk,))
    if key:
        cache.delete(key)
