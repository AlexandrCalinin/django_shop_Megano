from beartype import beartype
from django.db.models import Sum, QuerySet

from cart_app.models import CartItem, Cart
from catalog_app.models import Product
from core.models import Seller
from interface.cartitem_interface import ICartItem


class CartItemRepository(ICartItem):

    @beartype
    def save(self, model: CartItem) -> None:
        model.save()

    @beartype
    def create_cartitem(self, _cart: Cart, _product: Product, _count: str, _amount: str, _seller: Seller) -> None:
        """Создать CartItem"""
        CartItem.objects.create(cart_id=_cart,
                                product=_product,
                                count=_count,
                                amount=_amount,
                                seller=_seller)

    @beartype
    def get_by_cart_id(self, _cart: Cart) -> QuerySet[CartItem]:
        """Получить CartItem"""
        return CartItem.objects.filter(cart_id=_cart)

    @beartype
    def get_by_product_id(self, _product: str, _cart: Cart):
        """Получить продукт из cartitem"""
        return CartItem.objects.filter(product=_product,
                                       cart_id=_cart).first()

    def get_count_amount(self, _cart: Cart) -> CartItem:
        """Получить количество продуктов и сумму"""
        return CartItem.objects.filter(cart_id=_cart).aggregate(Sum('count'), Sum('amount'))

    def delete_product(self, _product: str) -> None:
        """Удалить объект"""
        CartItem.objects.filter(product=_product).first().delete()
