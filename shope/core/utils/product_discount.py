import inject
from django.utils.translation import gettext as _

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
        if dct_group_sales:
            priority = min(dct_group_sales)
            return_dct = dct_group_sales

        dct_cart_sale = self._cart_sales.possible_get_discount(_cart_item_qs=cart_item_qs)
        if dct_cart_sale and priority > dct_cart_sale.priority:
            priority = dct_cart_sale.priority
            return_dct = {dct_cart_sale.priority: {}}
            for product_id in product_id_lst:
                return_dct[dct_cart_sale.priority][product_id] = [dct_cart_sale, [_(
                    f'Discount on the shopping cart has been applied! Benefit {dct_cart_sale.value} %')]]

        dct_product_sale = dict()
        for product_id in product_id_lst:
            sales = self.get_all_discount_on_product(product_id)
            if sales:
                sale = sales.order_by('-value').first()
                dct_product_sale[sale.priority] = dct_product_sale.get(sale.priority, {product_id: sale})
                dct_product_sale[sale.priority][product_id] = [sale, [_(
                    f'The discount on the product has been applied! Benefit {sale.value} %')]]
        if dct_product_sale and priority >= min(dct_product_sale):
            return_dct = dct_product_sale

        new_return_lst = []
        for key, value in list(return_dct.values())[0].items():
            dct = dict()
            dct['product_id'] = key
            dct['sale_model'] = value[0]
            dct['message'] = ''
            if value[0]:
                dct['message'] = value[1][-1]
            new_return_lst.append(dct)

        return new_return_lst

    def calculate_price_with_discount(self):
        """
        рассчитать цену со скидкой на товар
        """
        pass
