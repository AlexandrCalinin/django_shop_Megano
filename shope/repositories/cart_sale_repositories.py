from typing import Optional

from beartype import beartype
from beartype.typing import Dict
from django.db.models import QuerySet, Sum, Max, F

from catalog_app.models import CartSale
from interface.cart_sale_interface import ICartSale


class CartSaleRepository(ICartSale):

    @beartype
    def get_list(self) -> QuerySet[CartSale]:
        """Вернуть кверисет скидок на продукт"""
        return CartSale.objects.all()

    @beartype
    def possible_get_discount(self, _cart_item_qs: QuerySet) -> Optional[CartSale]:
        """Вернуть возможность применения скидки"""
        qs = _cart_item_qs.values('product__id', 'count', 'amount')
        total_amount = sum([dct['amount'] for dct in qs])
        total_count = _cart_item_qs.aggregate(num=Sum('count'))
        total_count = total_count['num']
        print(total_amount, total_count)
        sale_qs = self.get_list().filter(quantity__lte=total_count, amount__lte=total_amount).order_by('-value').first()
        print(sale_qs)
        if not sale_qs:
            return None
        return sale_qs
