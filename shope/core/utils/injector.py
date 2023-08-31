import inject

from interface.discount_interface import IDiscountBaseModel
from interface.order_interface import IOrder
from repositories.discount_repositories import DiscountBaseModelRepository
from repositories.order_repositories import OrderRepository

BINDS = (
    (IOrder, OrderRepository),
    (IDiscountBaseModel, DiscountBaseModelRepository),

)


def config(binder):
    """Конфигуратор для inject."""
    for interface, implementation in BINDS:
        binder.bind(interface, implementation())


def configure_inject():
    """Конфигурирует зависимости для проекта."""
    inject.configure_once(config)
