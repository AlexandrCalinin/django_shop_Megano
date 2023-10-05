import random
from typing import Any
from beartype import beartype

from django.db.models import QuerySet, Sum, Q, Avg, Min, Max, FloatField
from django.db.models import Func
from django.db.models.functions import Cast


from catalog_app.models import Product
from interface.product_interface import IProduct


class Round(Func):
    function = 'ROUND'
    template = '%(function)s(%(expressions)s, 2)'


class ProductRepository(IProduct):

    def get_product_top_list(self, const: int) -> QuerySet[Product]:
        """Вернуть кверисет популярных продуктов"""
        qs = Product.objects.filter(is_active=True, orderitem__count__gte=1).annotate(
            qty=Sum('orderitem__count'),
            value=Round(Cast(Min('price__price'), output_field=FloatField()))
        ).order_by('-qty')[:const]
        if len(qs) < const:
            qs = Product.objects.filter(~Q(id__in=qs), is_active=True, price__price__gte=1).annotate(
                value=Round(Cast(Min('price__price'), output_field=FloatField())))[:const - 0]
        return qs

    def get_product_limit_list(self, const: int) -> QuerySet[Product]:
        """Вернуть кверисет лимитированых продуктов"""
        qs = Product.objects.filter(is_active=True, is_limited=True).annotate(
            min_price=Round(Cast(Min('price__price'), output_field=FloatField())),
            max_price=Round(Cast(Max('price__price'), output_field=FloatField())),
            value=Round(Cast(Avg('price__price'), output_field=FloatField()))
        )
        if len(qs) > const:
            const_num_list = random.sample([product.pk for product in qs], const)
            qs = qs.filter(product__id__in=const_num_list)
        return qs

    @beartype
    def get_sellers_of_product(self, _pk: int) -> list:
        """Получить список продавцов, которые продают данный продукт"""
        distinct = list(Product.objects.filter(pk=1).values('price__seller').distinct())
        return distinct
