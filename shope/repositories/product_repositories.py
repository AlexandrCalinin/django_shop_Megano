import random

from beartype import beartype
from django.db.models import QuerySet, Sum, Q, Avg, Min, Max, F, FloatField, OuterRef, Subquery
from django.db.models import Func
from django.db.models.functions import Cast

from catalog_app.models import Product
from core.models import Price
from interface.product_interface import IProduct


class Round(Func):
    function = 'ROUND'
    template = '%(function)s(%(expressions)s, 0)'


class ProductRepository(IProduct):

    def get_product_top_list(self, const: int) -> QuerySet[Product]:
        """Вернуть кверисет популярных продуктов"""
        qs = Product.objects.filter(is_active=True, orderitem__count__gte=1).annotate(
            qty=Sum('orderitem__count'),
            min_price=Round(Cast(Min('price__price'), output_field=FloatField())),
            seller_id=F('price__seller_id')
        ).order_by('-qty')[:const]
        if len(qs) < const:
            min_price_subquery = Price.objects.filter(product=OuterRef('pk')).values('product').annotate(
                min_value=Min('price')
            ).values('min_value')[:1]
            min_price_seller_subquery = Price.objects.filter(
                product=OuterRef('pk'), price=OuterRef('min_price')
            ).values('seller_id')[:1]
            qs = Product.objects.annotate(
                min_price=Subquery(min_price_subquery.values('min_value'), output_field=FloatField()),
                min_price_seller_id=Subquery(min_price_seller_subquery)
            ).filter(min_price__gt=0)[:const - 0]

        return qs

    def get_product_limit_list(self, const: int) -> QuerySet[Product]:
        """Вернуть кверисет лимитированых продуктов"""
        qs = Product.objects.filter(is_active=True, is_limited=True).annotate(
            min_price=Round(Min('price__price')),
            max_price=Round(Max('price__price')),
            value=Round(Avg('price__price'))
        )
        if len(qs) > const:
            const_num_list = random.sample([product.pk for product in qs], const)
            qs = qs.filter(product__id__in=const_num_list)
        return qs

    @beartype
    def get_by_id(self, product: str) -> Product:
        """Получить продукт по id"""
        return Product.objects.get(product)
