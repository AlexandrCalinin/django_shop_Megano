from abc import abstractmethod

from django.db.models import QuerySet

from catalog_app.models import DiscountProduct, DiscountProductGroup, CartSale
from core.models.base_discount import DiscountBaseModel


class IDiscountBaseModel:

    @abstractmethod
    def save(self, model: DiscountBaseModel) -> None:
        """Сохранить скидку."""
        pass


class IDiscountProduct:

    @abstractmethod
    def get_object_list(self, model: DiscountProduct) -> QuerySet[DiscountProduct]:
        """Получить кверисет скидок на продукт"""
        pass


class IDiscountProductGroup:

    @abstractmethod
    def get_object_list(self, model: DiscountProductGroup) -> QuerySet[DiscountProductGroup]:
        """Получить кверисет скидок на группу продуктов"""
        pass


class ICartSale:

    @abstractmethod
    def get_object_list(self, model: CartSale) -> QuerySet[CartSale]:
        """Получить кверисет скидок на корзину"""
        pass
