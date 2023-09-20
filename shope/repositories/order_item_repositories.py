""" Order item repositories"""
from beartype import beartype
from django.db.models import QuerySet

from interface.order_item_interface import IOrderItem
from order_app.models import Order, OrderItem


class OrderItemRepository(IOrderItem):

    @beartype
    def get_by_order(self, _order: Order) -> QuerySet[OrderItem]:
        """Получить продкуты по заказу."""
        return OrderItem.objects.filter(order=_order).select_related('product')
