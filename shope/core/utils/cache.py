""" Кеширование сайта """

from django.http import HttpRequest
from django.urls import reverse
from django.utils.cache import get_cache_key
from django.core.cache import cache
from django.conf import settings


def invalidate_cache(path='', *args, namespace=None):
    """Удалить значение кеша по заданному пути"""
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
