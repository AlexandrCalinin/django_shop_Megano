""" Кеширование сайта """

from django.http import HttpRequest
from django.urls import reverse
from django.utils.cache import get_cache_key
from django.core.cache import cache
from django.conf import settings
from core.models import CacheSetup


def invalidate_cache(path='', *args, namespace=None):
    """Удалить значение кеша по заданному пути url для декоратора cache_page"""
    request = HttpRequest()
    request.META = {
        'SERVER_NAME': settings.SERVER_NAME,
        'SERVER_PORT': settings.SERVER_PORT
    }
    request.LANGUAGE_CODE = 'en-us'
    if namespace:
        path = namespace + ":" + path
    request.path = reverse(path, args=args)

    request.method = 'GET'

    try:
        cache_key = get_cache_key(request)
        if cache_key:
            if cache.has_key(cache_key):
                cache.delete(cache_key)
                return True
            else:
                return False
        else:
            raise ValueError('failed to create cache_key')
    except (ValueError, Exception):
        return False


def get_cache_value(cache_value: str) -> int:
    """Получить значение ключа для кеша"""

    try:
        cache_data = cache.get_or_set(cache_value,
                                      CacheSetup.objects.get(key=cache_value),
                                      settings.CACHE_VALUES['DEFAULT']
                                      )
    except CacheSetup.DoesNotExist:
        cache_data = CacheSetup(key=cache_value,
                                value=settings.CACHE_VALUES[cache_value])
        cache_data.save()
        cache.set(cache_value,
                  cache_data,
                  settings.CACHE_VALUES['DEFAULT']
                  )

    return cache_data.value
