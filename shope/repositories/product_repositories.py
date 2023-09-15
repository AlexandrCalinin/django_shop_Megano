from django.db.models import QuerySet, Sum, Q

from catalog_app.models import Product
from interface.product_interface import IProduct


class ProductRepository(IProduct):

    def get_product_top_list(self) -> QuerySet[Product]:
        """Вернуть кверисет популярных продуктов"""
        qs = Product.objects.filter(orderitem__count__gte=1).annotate(qty=Sum('orderitem__count')).order_by('-qty')[:8]
        qs_id = []
        if len(qs) < 8:
            qs_id = Product.objects.filter(~Q(id__in=qs))[:8 - len(qs)]
        return list(qs) + list(qs_id)
