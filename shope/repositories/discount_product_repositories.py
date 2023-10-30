from django.db.models import QuerySet, Q, F

from catalog_app.models import DiscountProduct
from interface.discount_product_interface import IDiscountProduct


class DiscountProductRepository(IDiscountProduct):

    def get_list(self) -> QuerySet[DiscountProduct]:
        """Вернуть кверисет скидок на продукт"""
        return DiscountProduct.objects.all()

    def get_list_by_id(self, _id: int) -> QuerySet[DiscountProduct]:
        """Вернуть кверисет скидок на продукт по id"""
        return DiscountProduct.objects.filter(is_active=True).filter(
            Q(product__id=_id) | Q(category__product__id=_id)
        )
