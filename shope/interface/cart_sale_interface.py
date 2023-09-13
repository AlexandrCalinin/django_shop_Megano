from abc import abstractmethod

from django.db.models import QuerySet

from catalog_app.models import CartSale


class ICartSale:

    @abstractmethod
    def get_list(self) -> QuerySet[CartSale]:
        """Получить кверисет скидок на корзину"""
        pass
