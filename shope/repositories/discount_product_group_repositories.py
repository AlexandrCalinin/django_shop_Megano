from beartype import beartype
from django.db.models import QuerySet

from catalog_app.models import DiscountProductGroup
from interface.discount_product_group_interface import IDiscountProductGroup


class DiscountProductGroupRepository(IDiscountProductGroup):

    @beartype
    def get_list(self) -> QuerySet[DiscountProductGroup]:
        """Вернуть кверисет скидок на продукт"""
        return DiscountProductGroup.objects.all()

    @beartype
    def possible_get_discount(self, _product_id_list: [int]) -> bool:
        """Вернуть возможность применения скидки"""
        qs = DiscountProductGroup.objects.filter(category__product__id__in=_product_id_list)
        if not qs:
            return False
        else:
            for sale in qs:
                for cat in sale.category.all():
                    print('cat', cat)
