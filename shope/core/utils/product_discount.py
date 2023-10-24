import inject

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

    def get_priority_discount(self, product_id_list):
        """
        получить приоритетную скидку на указанный список товаров или на один товар
        """
        if self._product_group_sales.possible_get_discount(_product_id_list=product_id_list):
            pass

    def calculate_price_with_discount(self):
        """
        рассчитать цену со скидкой на товар
        """
        pass
