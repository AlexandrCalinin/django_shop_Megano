from django.db.models import QuerySet

from catalog_app.models import DiscountProduct
from interface.discount_product_interface import IDiscountProduct


class DiscountProductRepository(IDiscountProduct):

    def get_list(self) -> QuerySet[DiscountProduct]:
        """Вернуть кверисет скидок на продукт"""
        return DiscountProduct.objects.all()
