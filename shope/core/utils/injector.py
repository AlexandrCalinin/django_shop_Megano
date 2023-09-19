import inject

from interface.cart_sale_interface import ICartSale
from interface.category_interface import ICategory
from interface.discount_interface import IDiscountBaseModel
from interface.discount_product_group_interface import IDiscountProductGroup
from interface.discount_product_interface import IDiscountProduct
from interface.order_interface import IOrder

from interface.product_interface import IProduct
from interface.product_viewed_interface import IProductViewed
from repositories.cart_sale_repositories import CartSaleRepository
from repositories.category_repositories import CategoryRepository
from repositories.discount_product_group_repositories import DiscountProductGroupRepository
from repositories.discount_product_repositories import DiscountProductRepository
from repositories.discount_repositories import DiscountBaseModelRepository
from interface.auth_interface import IAuth

from repositories.order_repositories import OrderRepository
from repositories.auth_repositories import AuthRepository
from repositories.product_repositories import ProductRepository
from repositories.product_viewed_repositories import ProductViewedRepository

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
    (IProduct, ProductRepository),
    (ICharacteristicProduct, CharacteristicRepository),
    (ICategory, CategoryRepository),
    # (ICatalogFilter, CatalogFilterRepository),
    (IProductViewed, ProductViewedRepository),
)


def config(binder):
    """Конфигуратор для inject."""
    for interface, implementation in BINDS:
        binder.bind(interface, implementation())


def configure_inject():
    """Конфигурирует зависимости для проекта."""
    inject.configure_once(config)
