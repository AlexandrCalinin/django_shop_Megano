import inject

from interface.order_interface import IOrder
from interface.auth_interface import IAuth
from repositories.order_repositories import OrderRepository
from repositories.auth_repositories import AuthRepository

BINDS = (
    (IOrder, OrderRepository),
    (IAuth, AuthRepository)
)


def config(binder):
    """Конфигуратор для inject."""
    for interface, implementation in BINDS:
        binder.bind(interface, implementation())


def configure_inject():
    """Конфигурирует зависимости для проекта."""
    inject.configure_once(config)
