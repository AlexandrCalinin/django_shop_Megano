import inject

from interface.discount_interface import IDiscountBaseModel, IDiscountProduct, IDiscountProductGroup, ICartSale
from interface.order_interface import IOrder
from repositories.discount_repositories import DiscountBaseModelRepository, DiscountProductRepository, \
    DiscountProductGroupRepository, CartSaleRepository
from interface.auth_interface import IAuth
from repositories.order_repositories import OrderRepository
from repositories.auth_repositories import AuthRepository

from repositories.profile_repositories import ProfileRepository
from interface.profile_interface import IProfile

from repositories.characterisic_repositories import CharacteristicRepository
from interface.characteristic_interface import ICharacteristicProduct

BINDS = (
    (IOrder, OrderRepository),
    (IDiscountBaseModel, DiscountBaseModelRepository),
    (IAuth, AuthRepository),
    (IDiscountProduct, DiscountProductRepository),
    (IDiscountProductGroup, DiscountProductGroupRepository),
    (ICartSale, CartSaleRepository),
    (IProfile, ProfileRepository),
    (ICharacteristicProduct, CharacteristicRepository),
)


def config(binder):
    """Конфигуратор для inject."""
    for interface, implementation in BINDS:
        binder.bind(interface, implementation())


def configure_inject():
    """Конфигурирует зависимости для проекта."""
    inject.configure_once(config)
