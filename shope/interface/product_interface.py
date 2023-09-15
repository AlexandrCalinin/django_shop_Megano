from abc import abstractmethod

from django.db.models import QuerySet

from catalog_app.models import Product


class IProduct:

    @abstractmethod
    def get_product_top_list(self) -> QuerySet[Product]:
        """Получить кверисет популярных продуктов"""
        pass
