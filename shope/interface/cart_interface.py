"""Интерфейсы для модели Cart"""
from abc import abstractmethod
from typing import Optional
from auth_app.models import User
from cart_app.models import Cart


class ICart:
    """ICart"""

    @abstractmethod
    def get_active_by_user(self, _user: User) -> Optional[Cart]:
        """Получить активную корзину пользоветеля."""
        pass

    @abstractmethod
    def save(self, _cart: Cart) -> None:
        """ Сохранить корзину."""
        pass
