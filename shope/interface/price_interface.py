from abc import abstractmethod
from typing import Any, List

from core.models.price import Price


class IPrice:

    @abstractmethod
    def get_last_minprice_dct(self, _product_id_lst: List):
        """Получить последнюю цену  продукта"""
        pass
