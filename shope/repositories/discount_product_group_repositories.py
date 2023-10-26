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
    def possible_get_discount(self, _cart_item_qs: QuerySet) -> Optional[Dict]:
        """Вернуть возможность применения скидки"""
        cat_id_qs = _cart_item_qs.values('product__category__id')
        print('cat_id_qs - категории - товары в корзине', cat_id_qs)
        cat_id_lst = [dct['product__category__id'] for dct in cat_id_qs]
        print('cat_id_lst - категории - товары в корзине', cat_id_lst)
        qs_cats = Category.objects.filter(discountproductgroup__category__in=cat_id_lst)
        print('qs_cats - Все категории входящие в групповую скидку, связанную с категорией в корзине', qs_cats)
        qs = qs_cats.filter(id__in=cat_id_lst).distinct()
        print('qs - Уникальные категории входящие в корзину и в групповую скидку', qs)
        dct = dict()
        flag = False
        for cat in qs:
            sale = DiscountProductGroup.objects.get(category__id=cat.id)
            if sale:
                dct[sale.priority] = dct.get(sale.priority, {sale._meta.model_name: {sale.id: 0}})
                if not dct[sale.priority][sale._meta.model_name].get(sale.id, None):
                    dct[sale.priority][sale._meta.model_name] = {sale.id: 0}
                dct[sale.priority][sale._meta.model_name][sale.id] += 1
                if dct[sale.priority][sale._meta.model_name][sale.id] > 1:
                    flag = True
        # new_dct = {}
        if flag:
            # product_id_qs = _cart_item_qs.values('product__id', 'count')
            # product_id_lst = [dct['product__id'] for dct in product_id_qs]

            return dct
        return None
