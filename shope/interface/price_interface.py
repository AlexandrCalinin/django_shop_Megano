from abc import abstractmethod

from core.models import Price


class IPrice:

    @abstractmethod
    def save(self, model: Price) -> None:
        """Сохранить цену."""
        pass

    @abstractmethod
    def get_by_product_and_seller(self, product_id: str, seller_id) -> Price:
        """Получить цену по продукту и продавцу"""
        pass