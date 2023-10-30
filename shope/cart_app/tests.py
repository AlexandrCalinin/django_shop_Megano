from django.test import TestCase

from auth_app.models import User
from cart_app.models import Cart, CartItem
from catalog_app.models import Product


class CartListViewTestCase(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.user = User.objects.create(
            username='unittest_user',
            email='usertest@usertest.com',
            password='1q2w3e4r+'
        )
        cls.cart = Cart.objects.create(cls.user)
        cls.cartitem = CartItem.objects.create(cls.cart)
        cls.product = Product.objects.create(
            title='VideoCart',
            description='Some videocart',
            name='VideoCart',
            
        )