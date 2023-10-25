import inject
from django.db.models import Count, Sum, F

from interface.cart_sale_interface import ICartSale
from interface.discount_product_group_interface import IDiscountProductGroup
from interface.discount_product_interface import IDiscountProduct


class ProductDiscount:
    _product_sales: IDiscountProduct = inject.attr(IDiscountProduct)
    _product_group_sales: IDiscountProductGroup = inject.attr(IDiscountProductGroup)
    _cart_sales: ICartSale = inject.attr(ICartSale)

    def get_all_discount_on_product(self, product_id):
        """
        получать все скидки на товар
        """
        return self._product_sales.get_list_by_id(_id=product_id)

    def get_priority_discount(self, cart_item_qs):
        """
        получить приоритетную скидку на указанный список товаров или на один товар
        """
        cat_id_qs = cart_item_qs.values('product__category__id')
        cat_id_lst = [dct['product__category__id'] for dct in cat_id_qs]
        dct_group_sales = self._product_group_sales.possible_get_discount(_cat_id_list=cat_id_lst)
        print(dct_group_sales)
        # if dct_group_sales:
        #     return dct_group_sales
        product_id_qs = cart_item_qs.values('product__id', 'count')
        product_id_lst = [dct['product__id'] for dct in product_id_qs]
        # total_count = sum(dct['count'] for dct in product_id_qs)
        total_count = cart_item_qs.aggregate(num=Sum('count'))
        print(product_id_qs, product_id_lst, total_count)
        dct_cart_sale = self._cart_sales.possible_get_discount(_cart_item_qs=cart_item_qs)
        if dct_cart_sale:
            return dct_cart_sale

    def calculate_price_with_discount(self):
        """
        рассчитать цену со скидкой на товар
        """
        pass
