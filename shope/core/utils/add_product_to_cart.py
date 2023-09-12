from django.http import HttpResponse

from auth_app.models import User
from repositories.cart_repositories import CartRepository
from repositories.cartitem_repositories import CartItemRepository
from core.models import Seller


class AddProductToCart:

    def add_product_to_cart(self, data: dict, user: User) -> tuple[int, int]:
        """добавить товар в корзину"""
        cart = CartRepository()
        cartitem = CartItemRepository()

        if not cart.filter_by_user(_user=user):
            cart.create_user(_user=user)

        cart = cart.get_by_user(_user=user)
        cartitem_product = cartitem.get_by_cart_id(_cart=cart)

        product = data['product']
        product_count = data['count']
        amount = data['amount']
        seller = data['seller']

        cartitem.create_cartitem(_cart=cart, _product=product, _count=product_count,
                                 _amount=amount, _seller=seller)

        summ = 0
        count = 0
        for item in cartitem_product:
            count += item.count
            summ += item.amount

        return summ, count

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

    def get_list_in_cart(self):
        """
        получить список товаров в корзине
        """
        pass

    def get_count_product_in_cart(self):
        """
        получить кол-во товаров в корзине
        """
        pass
