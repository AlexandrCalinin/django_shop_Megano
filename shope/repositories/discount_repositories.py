from beartype import beartype
from django.utils.translation import gettext_lazy as _

from interface.discount_interface import IDiscountBaseModel
from core.models.base_discount import DiscountBaseModel


class DiscountBaseModelRepository(IDiscountBaseModel):

    @beartype
    def save(self, model: DiscountBaseModel) -> None:
        if model.value >= 99:
            raise Exception(_('The value of discount is more than the maximum! Max value is 99'))
        model.save()
