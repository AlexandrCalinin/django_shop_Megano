"""Order item interface"""

from abc import abstractmethod
from django.db.models import QuerySet

from order_app.models import OrderItem, Order


class IOrderItem:
    """Order item"""

    @abstractmethod
    def get_by_order(self, _order: Order) -> QuerySet[OrderItem]:
        """Получить продкуты по заказу."""
        pass
