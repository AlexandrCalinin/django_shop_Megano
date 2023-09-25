from abc import abstractmethod


from cart_app.models import Cart
from auth_app.models import User


class ICart:

    @abstractmethod
    def save(self, model: Cart) -> None:
        """сохранить корзину"""
        pass

    @abstractmethod
    def get_by_user(self, _user: User) -> Cart:
        """Получить корзину"""
        pass

    @abstractmethod
    def create_cart(self, _user: User) -> None:
        """Создать корзину"""
        pass


