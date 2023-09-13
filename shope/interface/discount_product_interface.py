from abc import abstractmethod

from django.db.models import QuerySet

from catalog_app.models import DiscountProduct


class IDiscountProduct:

    @abstractmethod
    def get_list(self) -> QuerySet[DiscountProduct]:
        """Получить кверисет скидок на продукт"""
        pass
