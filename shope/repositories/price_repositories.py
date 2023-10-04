from beartype import beartype

from core.models import Price
from interface.price_interface import IPrice


class PriceRepository(IPrice):

    @beartype
    def save(self, model: Price) -> None:
        """Сохранить цену"""
        model.save()

    @beartype
    def get_by_product_and_seller(self, product_id: str, seller_id) -> Price:
        """Получить цену по продукту и продавцу"""
        return Price.objects.filter(product=product_id,
                                    seller=seller_id).last()
