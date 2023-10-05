from beartype import beartype
from django.db.models import QuerySet

from catalog_app.models import CompareProduct
from interface.compare_product_interface import ICompareProduct


class CategoryRepository(ICompareProduct):

    @beartype
    def get_compare_product_list(self, const: int) -> QuerySet[CompareProduct]:
        """Вернуть кверисет продуктов для сравнения"""
        pass

    @beartype
    def create_compare_product(self, _product_id: int, _session_key: str) -> None:
        """Создать продукт для сравнения"""
        CompareProduct.objects.create(product_id=_product_id, session_key=_session_key)
