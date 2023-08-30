from beartype import beartype
from django.db.models import QuerySet

from interface.order_interface import IOrder
from order_app.models import Order


class OrderRepository(IOrder):

    @beartype
    def save(self, model: Order) -> None:
        model.save()

    @beartype
    def get_by_id(self, _id: int) -> Order:
        """Вернуть объект заказа."""

        return Order.objects.get(_id)

    @beartype
    def get_by_name(self, _name: str) -> QuerySet[Order]:
        """Вернуть объект заказа."""

        return Order.objects.filter(name=_name)
