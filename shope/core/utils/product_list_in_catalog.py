from catalog_app.models import Product
from core.models import Price


class ProductListCatalog:
    """Отобразить каталог с самой низкой ценной на продукт"""

    @staticmethod
    def product_list() -> list:

        product = Product.objects.all()
        price_list = []

        for product_id in product:
            queryset_price = Price.objects.filter(product=product_id)
            if len(queryset_price) > 1:
                min_price = queryset_price[0]
                for price in queryset_price:
                    if price.price < min_price.price:
                        min_price = price

                price_list.append(min_price)

            else:
                price_list.append(queryset_price[0])

        return price_list
