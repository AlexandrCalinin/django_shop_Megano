from beartype import beartype
from django.db.models import QuerySet

from auth_app.models import User
from interface.cart_interface import ICart
from cart_app.models import Cart

class CartRepository(ICart):

    @beartype
    def save(self, model: Cart) -> None:
        model.save()

    @beartype
    def get_by_user(self, _user: User) -> Cart:
        """Вернуть объект корзины."""

        return Cart.objects.get(user=_user)


    @beartype
    def filter_by_user(self, _user: User) -> QuerySet[Cart]:
        """Вернуть объект корзины."""

        return Cart.objects.filter(user=_user)

    @beartype
    def create_user(self, _user: User) -> None:
        """Создвать корзину"""
        Cart.objects.create(user=_user)
