from typing import Optional

from beartype import beartype
from beartype.typing import Dict
from django.db.models import QuerySet, Count

from catalog_app.models import DiscountProductGroup, Category
from interface.discount_product_group_interface import IDiscountProductGroup


class DiscountProductGroupRepository(IDiscountProductGroup):

    @beartype
    def get_list(self) -> QuerySet[DiscountProductGroup]:
        """Вернуть кверисет скидок на продукт"""
        return DiscountProductGroup.objects.all()

    @beartype
    def possible_get_discount(self, _cat_id_list: list) -> Optional[Dict]:
        """Вернуть возможность применения скидки"""
        qs_cats = Category.objects.filter(discountproductgroup__category__in=_cat_id_list)
        qs = qs_cats.filter(id__in=_cat_id_list).distinct()
        dct = dict()
        flag = False
        for cat in qs:
            sale = DiscountProductGroup.objects.get(category__id=cat.id)
            if sale:
                dct[sale.id] = dct.get(sale.id, 0) + 1
                if dct[sale.id] > 1:
                    flag = True
        if flag:
            return dct
        return None
