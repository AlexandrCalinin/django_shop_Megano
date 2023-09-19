from beartype import beartype
from django.db.models import QuerySet

from catalog_app.models import ProductViewed
from interface.product_viewed_interface import IProductViewed


class ProductViewedRepository(IProductViewed):
    @beartype
    def get_product_viewed_list(self, _user_id: int) -> QuerySet[ProductViewed]:
        """Вернуть кверисет просмотренных продуктов"""
        return ProductViewed.objects.filter(user_id=_user_id)
