from abc import abstractmethod

from order_app.models import Order


class IOrder:

    @abstractmethod
    def save(self, model: Order) -> None:
        """Сохранить заказ."""
        pass

    @abstractmethod
    def get_by_id(self, _id: int) -> Order:
        """Получить заказ."""
        pass


    @abstractmethod
    def get_by_name(self, _name: str) -> Order:
        """Получить заказ."""
        pass