import inject
from core.utils.injector import configure_inject

from auth_app.models import User
from cart_app.models import CartItem
from catalog_app.models import Product
from core.models import Seller, Price

from interface.cartitem_interface import ICartItem
from interface.cart_interface import ICart
from interface.product_interface import IProduct
from interface.price_interface import IPrice
from interface.seller_interface import ISeller

configure_inject()


class AddProductToCart:
    _cart: ICart = inject.attr(ICart)
    _cartitem: ICartItem = inject.attr(ICartItem)
    _product: IProduct = inject.attr(IProduct)
    _price: IPrice = inject.attr(IPrice)
    _seller: ISeller = inject.attr(ISeller)

    def add_product_to_cart(self, user: User, **kwargs) -> None:
        """добавить товар в корзину"""

        product_id, product_name, image, product_count, amount, seller_id = kwargs.values()

        cart = self._cart.get_active_by_user(_user=user)
        if not cart:
            cart = self._cart.create_cart(user)
        product = self._product.get_by_id(product_id)
        seller = self._seller.get_by_id(seller_id)

        if self._cartitem.get_by_product_id(_product=product_id, _cart=cart):
            self.change_count_product_in_cart(user=user,
                                              product=product_id,
                                              count=product_count,
                                              seller=seller)
        else:
            self._cartitem.create_cartitem(_cart=cart,
                                           _product=product,
                                           _count=product_count,
                                           _amount=amount,
                                           _seller=seller)

    @staticmethod
    def add_product_for_anonymous_user(request, **kwargs):
        """
        добавить товар в корзину для не зарегистрированного пользователя
        """
        product, product_name, image, product_count, amount, seller = kwargs.values()

        product_info = {'product': product, 'product_name': product_name,
                        'image': image, 'count': product_count,
                        'amount': amount, 'price': amount, 'seller': seller}

        if 'cart' in request.session:

            if not product in request.session["cart"]:  # сохраняем товары в сессию если такого товара нету в корзине
                request.session["cart"][product] = product_info
            else:  # если есть то прибаляем ко-во товаров
                request.session["cart"][product]['count'] = \
                    int(request.session["cart"][product]['count']) + int(product_count)

                request.session["cart"][product]['amount'] = \
                    float(request.session["cart"][product]['amount']) + float(amount)

        else:
            request.session["cart"] = {}
            request.session["cart"][product] = product_info
        request.session.modified = True

    def remove_product_from_cart(self, product, request):
        """
        убрать товар из корзины
        """

        if request.user.is_authenticated:
            self._cartitem.delete_product(_product=product)
        else:

            del request.session['cart'][product]
            request.session.modified = True

    def change_count_product_in_cart(self, user, **kwargs):
        """
        изменить кол-во товаров в корзине
        """
        cart = self._cart.get_active_by_user(_user=user)
        product, count, seller = kwargs.values()

        price = self._price.get_by_product_and_seller(product_id=product,
                                                      seller_id=seller)

        product_i = self._cartitem.get_by_product_id(_product=product,
                                                     _cart=cart)

        product_i.count += int(count)
        if count == '1':
            product_i.amount += price.price
        else:
            product_i.amount -= price.price

        product_i.save()
        return product_i

    @staticmethod
    def change_count_for_anonymous(request, **kwargs):
        """
        изменить кол-во товаров в корзине для не зарегистрированного пользователя
        """

        product, get_count, seller = kwargs.values()

        request.session["cart"][product]['count'] = \
            int(request.session["cart"][product]['count']) + int(get_count)

        if get_count == '1':
            request.session["cart"][product]['amount'] = \
                float(request.session["cart"][product]['amount']) + float(request.session["cart"][product]['price'])
        else:
            request.session["cart"][product]['amount'] = \
                float(request.session["cart"][product]['amount']) - float(request.session["cart"][product]['price'])

        request.session.modified = True
        return request.session["cart"][product]

    def get_list_in_cart(self, request) -> CartItem or None:
        """
        получить список товаров в корзине
        """

        if request.user.is_authenticated:
            cart = self._cart.get_active_by_user(_user=request.user)
            if not cart:
                return None
            return self._cartitem.get_by_cart_id(_cart=cart)
        else:
            products = request.session['cart']
            return products.values()

    def get_count_product_in_cart(self, user: User) -> tuple[int, int]:
        """
        получить кол-во товаров в корзине
        """
        cart = self._cart.get_active_by_user(_user=user)
        cart_products = self._cartitem.get_count_amount(_cart=cart)

        count, amount = cart_products.values()

        if count == None or amount == None:
            count = 0
            amount = 0

        return round(amount, 2), count

    @staticmethod
    def get_count_product_for_anonymous_user(request):
        """
        получить кол-во товаров в корзине для не зарегистрированного пользователя
        """
        try:
            products = request.session['cart']

            count = 0
            amount = 0
            for item in products.values():
                count += int(item['count'])
                amount += float(item['amount'])

            return round(amount, 2), round(count, 2)

        except KeyError:
            return 0, 0

    def create_cart_and_cartitem(self, user, request) -> None:
        """Создать корзину"""
        if self._cart.get_active_by_user(_user=user) == None:
            cart = self._cart.create_cart(_user=user)
        else:
            cart = self._cart.get_active_by_user(_user=user)

        if 'cart' in request.session:
            products = request.session['cart']
            for item, value in products.items():

                product = self._product.get_by_id(product=item)
                seller = Seller.objects.get(pk=value['seller'])

                count = value['count']
                amount = value['amount']

                self._cartitem.create_cartitem(_cart=cart,
                                               _product=product,
                                               _count=count,
                                               _amount=amount,
                                               _seller=seller)

            products.clear()
