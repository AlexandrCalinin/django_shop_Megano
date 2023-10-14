""" Интерфейс фильтрации каталога"""
from abc import abstractmethod
from typing import Any
from django.db.models import QuerySet

from catalog_app.models import Product


class ICatalogFilter:
    """Класс-репозиторий фильтрации товаров"""

    @abstractmethod
    def get_filtered_products(self, product_name: Any,
                              free_delivery: bool, is_limited: bool,
                              min_price: Any, max_price: Any) -> QuerySet[Product]:
        """Получить отфильтрованные продукты"""
        pass

    @abstractmethod
    def filter_by_tag(self, tag: Any) -> QuerySet[Product]:
        """Получить отфильтрованные продукты по тегам"""
        pass

    @abstractmethod
    def filter_by_sort(self, sort: Any) -> QuerySet[Product]:
        """Получить отфильтрованные продукты по критериям сортировки"""
        pass

    @abstractmethod
    def get_filtered_products_by_category(self, _category_id: str) -> QuerySet[Product]:
        """Получить отфильтрованные по категории продукты"""
        pass

    @abstractmethod
    def get_filtered_products_by_char(self, _char_id: str) -> QuerySet[Product]:
        """Получить отфильтрованные по Характеристике продукты"""
        pass
