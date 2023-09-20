""" Интерфейс фильтрации каталога"""
from abc import abstractmethod
from typing import Any
from django.db.models import QuerySet

from catalog_app.models import Product


class ICatalogFilter:
    """Класс-репозиторий фильтрации товаров"""

    @abstractmethod
    def get_filtered_products(self, product_name: Any,
                              free_delivery: bool, is_limited: bool) -> QuerySet[Product]:
        """Получить отфильтрованные продукты"""
        pass

    @abstractmethod
    def filter_by_tag(self, tag: Any) -> QuerySet[Product]:
        """Получить отфильтрованные продукты по тегам"""
        pass
