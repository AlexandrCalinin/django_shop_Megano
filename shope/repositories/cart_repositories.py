from beartype import beartype
from django.db.models import QuerySet

from interface.cart_interface import ICart
from cart_app.models import Cart

class CartRepository(ICart):

    @beartype
    def save(self, model: Cart) -> None:
        model.save()

    @beartype
    def get_by_user(self, _user_id: int) -> Cart:
        """Вернуть объект корзины."""

        return Cart.objects.get(user=_user_id)


    @beartype
    def filter_by_user(self, _user_id: int) -> QuerySet[Cart]:
        """Вернуть объект корзины."""

        return Cart.objects.filter(user=_user_id)

    @beartype
    def create_user(self, _user_id: int) -> None:
        """Создвать корзину"""
        Cart.objects.create(user=_user_id)
