""" Репозиторий фильтрации каталога"""
from typing import Any

from beartype import beartype
from django.db.models import QuerySet

from catalog_app.models import Product


class CatalogFilterRepository:
    """Класс-интерфейс фильтрации товаров"""

    @beartype
    def get_filtered_products(self, product_name: Any,
                              free_delivery: bool, is_limited: bool) -> QuerySet[Product]:
        """Получить отфильтрованные продукты"""
        if product_name is not None:
            if product_name is not None and free_delivery and is_limited:
                queryset = (Product.objects.prefetch_related('image', 'tag').
                            filter(title__icontains=product_name, is_delivery=free_delivery,
                                   is_limited=is_limited))
                return queryset

            elif product_name is not None and free_delivery:
                queryset = (Product.objects.prefetch_related('image', 'tag').
                            filter(title__icontains=product_name, is_delivery=free_delivery))
                return queryset

            elif product_name is not None and is_limited:
                queryset = (Product.objects.prefetch_related('image', 'tag').
                            filter(title__icontains=product_name, is_limited=is_limited))
                return queryset

            elif product_name is not None:
                queryset = (Product.objects.prefetch_related('image', 'tag').
                            filter(title__icontains=product_name))
                return queryset
        else:
            if free_delivery and is_limited:
                queryset = (Product.objects.prefetch_related('image', 'tag').
                            filter(is_delivery=free_delivery, is_limited=is_limited))
                return queryset

            elif free_delivery:
                queryset = (Product.objects.prefetch_related('image', 'tag').
                            filter(is_delivery=free_delivery))
                return queryset

            elif is_limited:
                queryset = (Product.objects.prefetch_related('image', 'tag').
                            filter(is_limited=is_limited))
                return queryset
            else:
                queryset = Product.objects.prefetch_related('image', 'tag')
                return queryset
