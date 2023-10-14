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
                                            is_active=is_limited,
                                            min_price__range=(product_min_price, product_max_price))

            elif free_delivery:
                return self.queryset.filter(title__icontains=product_name, is_delivery=free_delivery,
                                            min_price__range=(product_min_price, product_max_price))

            elif is_limited:
                return self.queryset.filter(title__icontains=product_name, is_active=is_limited,
                                            min_price__range=(product_min_price, product_max_price))

            else:
                return self.queryset.filter(title__icontains=product_name,
                                            min_price__range=(product_min_price, product_max_price))
        else:
            if free_delivery and is_limited:
                return self.queryset.filter(is_delivery=free_delivery, is_active=is_limited,
                                            min_price__range=(product_min_price, product_max_price))

            elif free_delivery:
                return self.queryset.filter(is_delivery=free_delivery,
                                            min_price__range=(product_min_price, product_max_price))

            elif is_limited:
                return self.queryset.filter(is_active=is_limited,
                                            min_price__range=(product_min_price, product_max_price))
            else:
                if not isinstance(product_min_price, str):
                    return self.queryset
                else:
                    return self.queryset.filter(min_price__range=(product_min_price, product_max_price))

    @beartype
    def filter_by_tag(self, tag_name: Any) -> QuerySet[Product]:
        tags = Tag.objects.filter(slug=tag_name).values_list('name', flat=True)
        return self.queryset.filter(tag__name__in=tags)

    @beartype
    def filter_by_sort(self, sort: Any) -> QuerySet[Product]:
        if sort == "min_price":
            return self.queryset.order_by(sort)
        else:
            return self.queryset.order_by(f"-{sort}")

    @beartype
    def get_filtered_products_by_category(self, _category_id: str) -> QuerySet[Product]:
        """Получить отфильтрованные по категории продукты"""
        return self.queryset.filter(is_active=True, category_id=int(_category_id))

    @beartype
    def get_filtered_products_by_char(self, _char_id: str) -> QuerySet[Product]:
        """Получить отфильтрованные по Характеристике продукты"""
        return self.queryset.filter(is_active=True, characteristics__characteristic_value__characteristic_type=int(_char_id))
