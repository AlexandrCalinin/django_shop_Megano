from typing import Any, List
from beartype import beartype
from django.db.models import DateTimeField, IntegerField, F
from django.db.models.functions import Cast
from django.utils import timezone

from core.models.price import Price
from interface.price_interface import IPrice


today = Cast(timezone.now().date(), output_field=DateTimeField())


class PriceRepository(IPrice):

    @beartype
    def get_last_minprice_dct(self, _product_id_lst: List):
        """Получить последнюю цену продукта"""
        qs = Price.objects.filter(product_id__in=_product_id_lst).values(
            'product_id', 'pk', 'price', 'seller', dure=Cast(today - F('seller__created_at'), output_field=IntegerField()))
        price_dict = dict()
        for dct in qs:
            last_date = dct['dure']
            if not price_dict.get(dct['product_id'], None):
                price_dict[dct['product_id']] = dct
            elif last_date < price_dict[dct['product_id']]['dure']:
                pass

        print(qs)
        return qs
