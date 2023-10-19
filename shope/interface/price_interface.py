from abc import abstractmethod
from beartype.typing import Any, List, Dict

from core.models.price import Price


class IPrice:

    @abstractmethod
    def get_last_minprice_dct(self, _product_id_lst: List) -> List[Dict] | None:
        """Получить последнюю цену  продукта"""
        pass
