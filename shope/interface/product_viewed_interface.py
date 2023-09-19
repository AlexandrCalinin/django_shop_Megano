from abc import abstractmethod

from django.db.models import QuerySet

from catalog_app.models import ProductViewed


class IProductViewed:

    @abstractmethod
    def get_product_viewed_list(self, _user_id: int) -> QuerySet[ProductViewed]:
        """Получить кверисет просмотренных продуктов"""
        pass
