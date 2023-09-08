from abc import abstractmethod


from cart_app.models import Cart


class ICart:

    @abstractmethod
    def save(self, model: Cart) -> None:
        """сохранить корзину"""
        pass

    @abstractmethod
    def get_by_user(self, _user_id: int) -> Cart:
        """Получить корзину"""
        pass

    @abstractmethod
    def filter_by_user(self, _user_id: int) -> Cart:
        """Вернуть объект объект корзины"""
        pass

    @abstractmethod
    def create_cart(self, _user_id: int) -> None:
        """Создать корзину"""
        pass

