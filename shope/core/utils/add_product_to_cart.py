import inject
from django.db.models import Sum

from cart_app.models import CartItem, Cart
from catalog_app.models import Product
from core.models import Seller, Price
from core.utils.injector import configure_inject

from auth_app.models import User
from interface.cartitem_interface import ICartItem
from interface.cart_interface import ICart


configure_inject()


class AddProductToCart:
    _cart: ICart = inject.attr(ICart)
    _cartitem: ICartItem = inject.attr(ICartItem)

    def add_product_to_cart(self, user: User, **kwargs) -> None:
        """добавить товар в корзину"""
        product_id, product_name, image, product_count, amount, seller_id = kwargs.values()

        cart = self._cart.get_by_user(_user=user)
        cartitem = self._cartitem.get_by_cart_id(_cart=cart)
        product = Product.objects.get(id=product_id)
        seller = Seller.objects.get(id=seller_id)

        try:
            cartitem.objects.get(product_id=product)
            self.change_count_product_in_cart(user, product=product_id, count=product_count, seller=seller)
        except Exception:
            self._cartitem.create_cartitem(_cart=cart, _product=product, _count=product_count,
                                           _amount=amount, _seller=seller)

    def remove_product_from_cart(self, request):
        """
        убрать товар из корзины
        """
        product = request.POST['product']
        if request.user.is_authenticated:
            CartItem.objects.get(product=product).delete()
        else:
            del request.session['cart'][product]

    def change_count_product_in_cart(self, user, **kwargs):
        """
        изменить кол-во товаров в корзине
        """
        cart = self._cart.get_by_user(_user=user)
        product, count, seller = kwargs.values()

        price = Price.objects.get(product=product, seller=seller)

        # product = self._cartitem.get_by_product_id(_product=product, _cart=cart)
        product_i = CartItem.objects.filter(product=product, cart_id=cart).first()

        product_i.count += int(count)
        if count == '1':
            product_i.amount += price.price
        else:
            product_i.amount -= price.price

        product_i.save()
        return product_i.amount

    def change_count_product_in_cart_for_anonymous(self, request, **kwargs) -> None:
        """
        изменить кол-во товаров в корзине для не зарегистрированного пользователя
        """

        product, count, seller = kwargs.values()
        request.session["cart"][product]['count'] = \
            int(request.session["cart"][product]['count']) + int(count)

    def get_list_in_cart(self, request) -> CartItem:
        """
        получить список товаров в корзине
        """
        if request.user.is_authenticated:
            cart = self._cart.get_by_user(_user=request.user)
            return self._cartitem.get_by_cart_id(_cart=cart)
        else:
            products = request.session['cart']
            return products.values()

    def get_count_product_in_cart(self, user: User) -> tuple[int,int]:
        """
        получить кол-во товаров в корзине
        """
        cart = self._cart.get_by_user(_user=user)
        cart_products = self._cartitem.get_count_amount(_cart=cart)

        count, amount = cart_products.values()

        return round(amount, 2), count

    def get_count_product_for_anonymous_user(self, request):
        """
        получить кол-во товаров в корзине для не зарегистрированного пользователя
        """
        try:
            products = request.session['cart']

            count = 0
            amount = 0
            for item in products.values():
                count += int(item['count'])
                amount += int(item['count']) * float(item['amount'])
            return round(amount, 2), round(count, 2)
        except KeyError:
            return 0, 0

    def add_product_for_anonymous_user(self, request, **kwargs):
        """
        добавилть товар в корзину для не зарегистрированного пользователя
        """
        product, product_name, image, product_count, amount, seller = kwargs.values()

        product_info = {'product': product, 'product_name': product_name,
                        'image': image, 'count': product_count,
                        'amount': amount, 'seller': seller}

        if 'cart' in request.session:
            if not product in request.session["cart"]:
                request.session["cart"][product] = product_info
            else:
                request.session["cart"][product]['count'] = \
                    int(request.session["cart"][product]['count']) + int(product_count)
        else:
            request.session["cart"] = {}
            request.session["cart"][product] = product_info
        request.session.modified = True

    def create_cart_and_cartitem(self, request) -> None:
        """Создать корзину"""
        try:
            cart = self._cart.get_by_user(_user=request.user)

        except:
            cart = self._cart.create_cart(request.user)

        products = request.session['cart']

        CartItem.objects.bulk_create([CartItem(cart_id=cart, product=item['product'],
                                               count=item['count'], amount=item['amount'],
                                               seller=item['seller']) for item in products.values()])
        products.clear()
