from beartype import beartype

from core.utils.exception import MaxDiscountErrorException
from interface.discount_interface import IDiscountBaseModel
from core.models.base_discount import DiscountBaseModel


class DiscountBaseModelRepository(IDiscountBaseModel):

    @beartype
    def save(self, model: DiscountBaseModel) -> None:
        if model.value >= 99:
            raise MaxDiscountErrorException
        model.save()
