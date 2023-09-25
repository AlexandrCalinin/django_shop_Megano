"""Репозитарий Cart"""
from typing import Optional
from beartype import beartype
from interface.cart_interface import ICart
from auth_app.models import User
from cart_app.models import Cart


class CartRepository(ICart):
    """CartItemRepository"""

    @beartype
    def get_active_by_user(self, _user: User) -> Optional[Cart]:
        """Получить активную корзину пользоветеля."""
        try:
            return Cart.objects.get(user=_user, is_active=True)
        except Cart.DoesNotExist:
            return None

    @beartype
    def save(self, _cart: Cart) -> None:
        """ Сохранить корзину."""
        _cart.save()
