import inject

from interface.cart_sale_interface import ICartSale
from interface.discount_interface import IDiscountBaseModel
from interface.discount_product_group_interface import IDiscountProductGroup
from interface.discount_product_interface import IDiscountProduct
from interface.order_interface import IOrder
from repositories.cart_sale_repositories import CartSaleRepository
from repositories.discount_product_group_repositories import DiscountProductGroupRepository
from repositories.discount_product_repositories import DiscountProductRepository
from repositories.discount_repositories import DiscountBaseModelRepository
from interface.auth_interface import IAuth
from repositories.order_repositories import OrderRepository
from repositories.auth_repositories import AuthRepository

from repositories.profile_repositories import ProfileRepository
from interface.profile_interface import IProfile

from interface.cart_interface import ICart
from interface.cartitem_interface import ICartItem
from repositories.cart_repositories import CartRepository
from repositories.cartitem_repositories import CartItemRepository

BINDS = (
    (IOrder, OrderRepository),
    (IDiscountBaseModel, DiscountBaseModelRepository),
    (IAuth, AuthRepository),
    (IDiscountProduct, DiscountProductRepository),
    (IDiscountProductGroup, DiscountProductGroupRepository),
    (ICartSale, CartSaleRepository),
    (IProfile, ProfileRepository),
    (ICart, CartRepository),
    (ICartItem, CartItemRepository),
)


def config(binder):
    """Конфигуратор для inject."""
    for interface, implementation in BINDS:
        binder.bind(interface, implementation())


def configure_inject():
    """Конфигурирует зависимости для проекта."""
    inject.configure_once(config)
