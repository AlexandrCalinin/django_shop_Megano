import random

from django.db.models import QuerySet, Sum, Q, Avg, Min, Max, F
from django.db.models import Func

from catalog_app.models import Product
from interface.product_interface import IProduct


class Round(Func):
    function = 'ROUND'
    template = '%(function)s(%(expressions)s, 0)'


class ProductRepository(IProduct):

    def get_product_top_list(self, const: int) -> QuerySet[Product]:
        """Вернуть кверисет популярных продуктов"""
        qs = Product.objects.filter(is_active=True, orderitem__count__gte=1).annotate(
            qty=Sum('orderitem__count')
        ).order_by('-qty')[:const].annotate(value=Round(Avg('price__price')))
        if len(qs) < const:
            qs = Product.objects.filter(~Q(id__in=qs), is_active=True, price__price__gte=1).annotate(
                value=Round(Avg('price__price'))
            )[:const - 0]
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
