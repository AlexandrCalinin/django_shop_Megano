from abc import abstractmethod
from decimal import Decimal

from cart_app.models import CartItem, Cart
from catalog_app.models import Product
from core.models import Seller


class ICartItem:

    @abstractmethod
    def save(self, model: CartItem) -> None:
        """Сохранить CartItem."""
        pass

    @abstractmethod
    def create_cartitem(self, _cart: Cart, _product: Product, _count: int, _amount: Decimal, _seller: Seller) -> None:
        """Создать CartItem"""
        pass

    @abstractmethod
    def get_by_cart_id(self, _cart: Cart) -> CartItem:
        """Получить CartItem"""
        pass

    @abstractmethod
    def get_by_product_id(self, _product: str, _cart: Cart) -> CartItem:
        """Получить CartItem"""
        pass

    @abstractmethod
    def get_count_amount(self, _cart: Cart) -> CartItem:
        """Получить количество продуктов и сумму"""
        pass

    @abstractmethod
    def delete_product(self, _product: str) -> None:
        """Удалить объект"""
        pass