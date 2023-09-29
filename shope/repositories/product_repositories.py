from django.db.models import QuerySet, Sum, Q, Min, F
from django.db.models import Func

from catalog_app.models import Product
from interface.product_interface import IProduct


class Round(Func):
    function = 'ROUND'
    template = '%(function)s(%(expressions)s, 0)'


class ProductRepository(IProduct):

    def get_product_top_list(self, const: int) -> QuerySet[Product]:
        """Вернуть кверисет популярных продуктов"""
        qs = Product.objects.filter(orderitem__count__gte=1).annotate(
            qty=Sum('orderitem__count')
        ).order_by('-qty')[:const].annotate(value=Round(Min('price__price')))
        if len(qs) < const:
            qs = Product.objects.filter(~Q(id__in=qs), is_active=True, price__price__gte=1).annotate(
                value=Round(Min('price__price'))
            )[:const - 0]
        return qs
