from decimal import Decimal

from beartype import beartype
from django.db.models import QuerySet

from cart_app.models import CartItem, Cart
from catalog_app.models import Product
from core.models import Seller
from interface.cartitem_interface import ICartItem


class CartItemRepository(ICartItem):

    @beartype
    def save(self, model: CartItem) -> None:
        model.save()

    @beartype
    def create_cartitem(self, _cart: Cart, _product: Product, _count: int, _amount: Decimal, _seller: Seller) -> None:
        """Создать CartItem"""
        CartItem.objects.create(cart_id=_cart, product=_product, count=_count, amount=_amount, seller=_seller)

    @beartype
    def get_by_cart_id(self, _cart: Cart) -> QuerySet[CartItem]:
        """Получить CartItem"""
        return CartItem.objects.filter(cart_id=_cart)