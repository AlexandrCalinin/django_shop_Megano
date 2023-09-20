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
                return (Product.objects.prefetch_related('image', 'tag').
                        filter(title__icontains=product_name, is_delivery=free_delivery,
                               is_limited=is_limited))

            elif product_name is not None and free_delivery:
                return (Product.objects.prefetch_related('image', 'tag').
                        filter(title__icontains=product_name, is_delivery=free_delivery))

            elif product_name is not None and is_limited:
                return (Product.objects.prefetch_related('image', 'tag').
                        filter(title__icontains=product_name, is_limited=is_limited))

            elif product_name is not None:
                return (Product.objects.prefetch_related('image', 'tag').
                        filter(title__icontains=product_name))
        else:
            if free_delivery and is_limited:
                return (Product.objects.prefetch_related('image', 'tag').
                        filter(is_delivery=free_delivery, is_limited=is_limited))

            elif free_delivery:
                return (Product.objects.prefetch_related('image', 'tag').
                        filter(is_delivery=free_delivery))

            elif is_limited:
                return (Product.objects.prefetch_related('image', 'tag').
                        filter(is_limited=is_limited))
            else:
                return Product.objects.prefetch_related('image', 'tag')

    @beartype
    def filter_by_tag(self, tag: Any) -> QuerySet[Product]:
        tags_dict = {
            '1': 'audio',
            '2': 'appliances',
            '3': 'tv',
            '4': 'telephones',
            '5': 'furniture',
            '6': 'video',
        }
        tag_name = tags_dict[tag]
        return Product.objects.prefetch_related('image', 'tag').filter(tag=tag_name).all()
