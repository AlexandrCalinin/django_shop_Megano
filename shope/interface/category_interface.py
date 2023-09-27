from abc import abstractmethod

from django.db.models import QuerySet

from catalog_app.models import Category


class ICategory:

    @abstractmethod
    def get_category_list(self) -> QuerySet[Category]:
        """Получить кверисет категорий"""
        pass

    @abstractmethod
    def get_min_price_of_category(self, _category_id: int) -> float:
        """Получить минимальную цену продукта категории"""
        pass
