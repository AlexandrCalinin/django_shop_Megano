from django.db.models import QuerySet

from catalog_app.models import CartSale
from interface.cart_sale_interface import ICartSale


class CartSaleRepository(ICartSale):

    def get_list(self) -> QuerySet[CartSale]:
        """Вернуть кверисет скидок на продукт"""
        return CartSale.objects.all()
