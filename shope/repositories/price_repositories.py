from beartype.typing import List, Dict
from beartype import beartype
from django.db.models import DateTimeField, IntegerField, F
from django.db.models.functions import Cast
from django.utils import timezone

from core.models.price import Price
from interface.price_interface import IPrice


today = Cast(timezone.now().date(), output_field=DateTimeField())


class PriceRepository(IPrice):

    @beartype
    def save(self, model: Price) -> None:
        """Сохранить цену"""
        model.save()

    @beartype
    def get_last_minprice_dct(self, _product_id_lst: List) -> List[Dict] | None:
        """Получить последнюю цену продавца продукта и минимальную цену продукта, если продавцов больше одного"""
        qs = Price.objects.filter(is_active=True, product_id__in=_product_id_lst).values(
            'product_id', 'price', 'seller', duration=Cast(today - Cast(F('created_at'), output_field=DateTimeField()
                                                                        ), output_field=IntegerField())
        )
        price_dict = dict()
        for dct in qs:
            last_date = dct['duration']
            min_price = dct['price']
            if not price_dict.get(dct['product_id'], None):
                price_dict[dct['product_id']] = dct
            elif (last_date < price_dict[dct['product_id']]['duration']) &\
                    (price_dict[dct['product_id']]['seller'] == dct['seller']):
                price_dict[dct['product_id']] = dct
            elif min_price < price_dict[dct['product_id']]['price']:
                price_dict[dct['product_id']] = dct

        return [val for key, val in price_dict.items()]

    @beartype
    def get_by_product_and_seller(self, product_id: str, seller_id) -> Price:
        """Получить цену по продукту и продавцу"""
        return Price.objects.filter(product=product_id,
                                    seller=seller_id).last()
