from abc import abstractmethod

from django.db.models import QuerySet

from catalog_app.models import CompareProduct


class ICompareProduct:

    @abstractmethod
    def get_compare_product_list(self, const: int) -> QuerySet[CompareProduct]:
        """Получить кверисет продуктов для сравнения"""
        pass

    @abstractmethod
    def create_compare_product(self, _product_id: int, _session_key: str) -> None:
        """Создать продукт для сравнения"""
        pass
