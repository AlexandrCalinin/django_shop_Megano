""" Репозиторий фильтрации каталога"""
from typing import Any

from beartype import beartype
from django.db.models import QuerySet, OuterRef, Min, Subquery

from catalog_app.models import Product
from core.models.price import Price


class CatalogFilterRepository:
    """Класс-интерфейс фильтрации товаров"""
    min_prices = Price.objects.filter(product=OuterRef('pk'), ).annotate(
        min_value=Min('price')
    ).values('min_value')[:1]
    queryset = Product.objects.annotate(
        min_price=Subquery(min_prices)
    ).filter(min_price__gt=0)

    @beartype
    def get_filtered_products(self, product_name: Any,
                              free_delivery: bool, is_limited: bool,
                              product_min_price: Any, product_max_price: Any) -> QuerySet[Product]:
        """Получить отфильтрованные продукты"""

        if product_name is not None:
            if product_name is not None and free_delivery and is_limited:
                return self.queryset.filter(title__icontains=product_name, is_delivery=free_delivery,
                                            is_limited=is_limited,
                                            min_price__gte=int(product_min_price),
                                            min_price__lte=int(product_max_price))

            elif product_name is not None and free_delivery:
                return self.queryset.filter(title__icontains=product_name, is_delivery=free_delivery,
                                            min_price__gte=int(product_min_price),
                                            min_price__lte=int(product_max_price))

            elif product_name is not None and is_limited:
                return self.queryset.filter(title__icontains=product_name, is_limited=is_limited,
                                            min_price__gte=int(product_min_price),
                                            min_price__lte=int(product_max_price))

            elif product_name is not None:
                return self.queryset.filter(title__icontains=product_name, min_price__gte=int(product_min_price),
                                            min_price__lte=int(product_max_price))
        else:
            if free_delivery and is_limited:
                return self.queryset.filter(is_delivery=free_delivery, is_limited=is_limited,
                                            min_price__gte=int(product_min_price),
                                            min_price__lte=int(product_max_price))

            elif free_delivery:
                return self.queryset.filter(is_delivery=free_delivery, min_price__gte=int(product_min_price),
                                            min_price__lte=int(product_max_price))

            elif is_limited:
                return self.queryset.filter(is_limited=is_limited, min_price__gte=int(product_min_price),
                                            min_price__lte=int(product_max_price))
            else:
                if not isinstance(product_min_price, str) and not isinstance(product_min_price, str):
                    return self.queryset
                else:
                    return self.queryset.filter(min_price__gte=int(product_min_price),
                                                min_price__lte=int(product_max_price))

    @beartype
    def filter_by_tag(self, tag: Any) -> QuerySet[Product]:
        # tags_dict = {
        #     '1': 'audio',
        #     '2': 'appliances',
        #     '3': 'tv',
        #     '4': 'telephones',
        #     '5': 'furniture',
        #     '6': 'video',
        # }
        return Product.objects.prefetch_related('image', 'tag')

    @beartype
    def filter_by_sort(self, sort: Any) -> QuerySet[Product]:
        # sort_dict = {
        #     '1': 'popularity',
        #     '2': 'price',
        #     '3': 'reviews',
        #     '4': 'novelty',
        # }
        return Product.objects.prefetch_related('image', 'tag')
