""" Репозиторий фильтрации каталога"""
from typing import Any

from beartype import beartype
from django.db.models import QuerySet, OuterRef, Min, Subquery
from taggit.models import Tag

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
            if free_delivery and is_limited:
                return self.queryset.filter(title__icontains=product_name, is_delivery=free_delivery,
                                            is_limited=is_limited,
                                            min_price__range=(product_min_price, product_max_price))

            elif free_delivery:
                return self.queryset.filter(title__icontains=product_name, is_delivery=free_delivery,
                                            min_price__range=(product_min_price, product_max_price))

            elif is_limited:
                return self.queryset.filter(title__icontains=product_name, is_limited=is_limited,
                                            min_price__range=(product_min_price, product_max_price))

            else:
                return self.queryset.filter(title__icontains=product_name,
                                            min_price__range=(product_min_price, product_max_price))
        else:
            if free_delivery and is_limited:
                return self.queryset.filter(is_delivery=free_delivery, is_limited=is_limited,
                                            min_price__range=(product_min_price, product_max_price))

            elif free_delivery:
                return self.queryset.filter(is_delivery=free_delivery,
                                            min_price__range=(product_min_price, product_max_price))

            elif is_limited:
                return self.queryset.filter(is_limited=is_limited,
                                            min_price__range=(product_min_price, product_max_price))
            else:
                if not isinstance(product_min_price, str):
                    return self.queryset
                else:
                    return self.queryset.filter(min_price__range=(product_min_price, product_max_price))

    @beartype
    def filter_by_tag(self, tag_name: Any) -> QuerySet[Product]:
        tags_dict = {
            '1': 'audio',
            '2': 'appliances',
            '3': 'tv',
            '4': 'telephones',
            '5': 'furniture',
            '6': 'video',
        }
        tags = Tag.objects.filter(slug=tags_dict[tag_name]).values_list('name', flat=True)
        return self.queryset.filter(tag__name__in=tags)

    @beartype
    def filter_by_sort(self, sort: Any) -> QuerySet[Product]:
        sort_dict = {
            '1': 'popularity',
            '2': 'min_price',
            '3': 'rewiew',
            '4': 'created_at',
        }
        return self.queryset.order_by(sort_dict[sort])

    @beartype
    def get_filtered_products_by_category(self, _category_id: str) -> QuerySet[Product]:
        """Получить отфильтрованные по категории продукты"""
        return self.queryset.filter(is_active=True, category_id=int(_category_id))
