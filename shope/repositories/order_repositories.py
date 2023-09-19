from beartype import beartype
from django.db.models import QuerySet

from interface.order_interface import IOrder
from order_app.models import Order
from auth_app.models import User


class OrderRepository(IOrder):

    @beartype
    def save(self, model: Order) -> None:
        model.save()

    @beartype
    def get_by_id(self, _id: int) -> Order:
        """Вернуть объект заказа."""

        return Order.objects.get(_id)

    def get_list_by_user(self, _user: User) -> QuerySet[Order]:
        """Получить список заказов пользоветеля."""

        return Order.objects.filter(user=_user)

    @beartype
    def get_last_by_user(self, _user: User) -> Order:
        """Получить последний заказ покупателя по дате создания"""

        return Order.objects.filter(user=_user).latest('created_at')
