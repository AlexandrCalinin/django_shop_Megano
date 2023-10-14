"""Signals for cache"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings


from catalog_app.models import Rewiew
from .utils.cache import invalidate_cache


@receiver(post_save, sender=Rewiew)
def create_review(sender, instance, **kwargs):
    """ Создание отзыва.
    Удаляем кеш детальной страницы продукта на странице которого создан отзыв"""

    invalidate_cache('product', instance.product_id)
