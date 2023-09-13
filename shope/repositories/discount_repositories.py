from beartype import beartype
from django.db.models import QuerySet

from catalog_app.models import DiscountProduct, DiscountProductGroup, CartSale
from core.utils.exception import MaxDiscountErrorException
from interface.discount_interface import IDiscountBaseModel, IDiscountProduct, IDiscountProductGroup, ICartSale
from core.models.base_discount import DiscountBaseModel


class DiscountBaseModelRepository(IDiscountBaseModel):

    @beartype
    def save(self, model: DiscountBaseModel) -> None:
        if model.value >= 99:
            raise MaxDiscountErrorException
        model.save()


class DiscountProductRepository(IDiscountProduct):

    @beartype
    def get_object_list(self, model: DiscountProduct) -> QuerySet[DiscountProduct]:
        """Вернуть кверисет скидок на продукт"""
        return DiscountProduct.objects.all()


class DiscountProductGroupRepository(IDiscountProductGroup):

    @beartype
    def get_object_list(self, model: DiscountProductGroup) -> QuerySet[DiscountProductGroup]:
        """Вернуть кверисет скидок на продукт"""
        return DiscountProductGroup.objects.all()


class CartSaleRepository(ICartSale):

    @beartype
    def get_object_list(self, model: CartSale) -> QuerySet[CartSale]:
        """Вернуть кверисет скидок на продукт"""
        return CartSale.objects.all()
