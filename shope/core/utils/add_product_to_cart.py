import inject

from cart_app.models import CartItem
from core.utils.injector import configure_inject

from auth_app.models import User
from interface.cartitem_interface import ICartItem
from interface.cart_interface import ICart


configure_inject()


class AddProductToCart:
    _cart: ICart = inject.attr(ICart)
    _cartitem: ICartItem = inject.attr(ICartItem)

    def add_product_to_cart(self, data: dict, user: User) -> None:
        """добавить товар в корзину"""

        if not self._cart.filter_by_user(_user=user):
            self._cart.create_user(_user=user)

        cart = self._cart.get_by_user(_user=user)


        product = data['product']
        product_count = data['count']
        amount = data['amount']
        seller = data['seller']

        self._cartitem.create_cartitem(_cart=cart, _product=product, _count=product_count,
                                 _amount=amount, _seller=seller)

    def remove_product_from_cart(self):
        """
        убрать товар из корзины
        """
        pass

    def change_count_product_in_cart(self):
        """
        изменить кол-во товаров в корзине
        """
        pass

    def get_list_in_cart(self, user: User) -> CartItem:
        """
        получить список товаров в корзине
        """
        cart = self._cart.get_by_user(_user=user)
        return self._cartitem.get_by_cart_id(_cart=cart)

    def get_count_product_in_cart(self, user: User) -> tuple[int,int]:
        """
        получить кол-во товаров в корзине
        """
        cart = self._cart.get_by_user(_user=user)
        cart_products = self._cartitem.get_by_cart_id(_cart=cart)

        summ = 0
        count = 0
        for item in cart_products:
            count += item.count
            summ += item.amount

        return summ, count
