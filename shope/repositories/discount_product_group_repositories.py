from django.db.models import QuerySet

from catalog_app.models import DiscountProductGroup
from interface.discount_product_group_interface import IDiscountProductGroup


class DiscountProductGroupRepository(IDiscountProductGroup):

    def get_list(self) -> QuerySet[DiscountProductGroup]:
        """Вернуть кверисет скидок на продукт"""
        return DiscountProductGroup.objects.all()
