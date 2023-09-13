from abc import abstractmethod

from django.db.models import QuerySet

from catalog_app.models import DiscountProductGroup


class IDiscountProductGroup:

    @abstractmethod
    def get_list(self) -> QuerySet[DiscountProductGroup]:
        """Получить кверисет скидок на группу продуктов"""
        pass
