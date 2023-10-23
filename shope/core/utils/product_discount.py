import inject

from interface.discount_product_interface import IDiscountProduct


class ProductDiscount:
    _product_sales: IDiscountProduct = inject.attr(IDiscountProduct)

    def get_all_discount_on_product(self, product_id):
        """
        получать все скидки на товар
        """
        return self._product_sales.get_list_by_id(_id=product_id)

    def get_priority_discount(self):
        """
        получить приоритетную скидку на указанный список товаров или на один товар
        """
        pass

    def calculate_price_with_discount(self):
        """
        рассчитать цену со скидкой на товар
        """
        pass
