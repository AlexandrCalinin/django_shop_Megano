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
        priority = 3
        product_id_qs = cart_item_qs.values('product__id', 'count')
        product_id_lst = [dct['product__id'] for dct in product_id_qs]
        return_dct = dict()

        dct_group_sales = self._product_group_sales.possible_get_discount(_cart_item_qs=cart_item_qs)
        print(dct_group_sales)
        if dct_group_sales:
            priority = min(dct_group_sales)
            return_dct = dct_group_sales

        dct_cart_sale = self._cart_sales.possible_get_discount(_cart_item_qs=cart_item_qs)
        print('dct_cart_sale', dct_cart_sale)
        if dct_cart_sale and priority > dct_cart_sale.priority:
            priority = dct_cart_sale.priority
            return_dct = dct_cart_sale

        dct_product_sale = dict()
        for product_id in product_id_lst:
            sales = self.get_all_discount_on_product(product_id)
            if sales:
                sale = sales.order_by('-value').first()
                dct_product_sale[sale.priority] = dct_product_sale.get(sale.priority, {product_id: sale})
                dct_product_sale[sale.priority][product_id] = sale
        if dct_product_sale and priority >= min(dct_product_sale):
            return_dct = dct_product_sale
            print('dct_product_sale', dct_product_sale)
        return return_dct

    def calculate_price_with_discount(self):
        """
        рассчитать цену со скидкой на товар
        """
        pass
