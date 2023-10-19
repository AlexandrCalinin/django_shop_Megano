"""Тестирование order_app"""

import os
from django.test import TestCase
from django.urls import reverse
from django.conf import settings

from django import setup

from core.enums import PayType, DeliveryType

from auth_app.models import User
from order_app.models import Order

from .utils_test import (
    create_orders_list,
    delete_orders_list,
    create_categories_list,
    delete_categories_list,
    create_products_list,
    delete_products_list,
    create_cart,
    delete_cart,
    create_seller,
    delete_seller,
    create_cart_items,
    delete_cart_items

)


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shope.settings')
setup()


class OrdersListViewTestCase(TestCase):
    """Тесты списка заказов"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.user = User.objects.create(
            username='unittest_user',
            email='usertest@usertest.com',
            password='1q2w3e4r+'
        )
        cls.orders = create_orders_list(cls.user)

    @classmethod
    def tearDownClass(cls) -> None:
        delete_orders_list(cls.orders)
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_order_list_view(self):
        """Получаем список заказов по первой странице пагинации максимум 3 заказа """

        response = self.client.get(reverse('order_app:history-order'))
        qs = Order.objects.filter(user=self.user).order_by('-created_at')[:3]
        self.assertQuerySetEqual(
            qs,
            values=(order.pk for order in response.context['order_list']),
            transform=lambda p: p.pk
        )

    def test_orders_list_not_authenticated(self):

        self.client.logout()
        response = self.client.get(reverse('order_app:history-order'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(str(settings.LOGIN_URL), response.url)


class OrderDetailsViewTestCase(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.user = User.objects.create(
            username='unittest_user',
            email='usertest@usertest.com',
            password='1q2w3e4r+'
        )
        cls.orders = create_orders_list(cls.user)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.user.delete()
        delete_orders_list(cls.orders)

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_get_one_order(self):
        """проверить страницу заказа
        проверям :
         - что в ответе статус 200;
         - что в контексте ответа тот же заказ, который был создан перед тестом (сравниваем по первичному ключу).
         _ что сумма заказ в ответе равна сумме созданного заказа
        """

        response = self.client.get(
            reverse('order_app:one-order', kwargs={'pk': self.orders[0].pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object'].pk, self.orders[0].pk)
        self.assertEqual(response.context['object'].amount, self.orders[0].amount)


class CreateOrderTestCase(TestCase):
    """Тесты создания заказа"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.user = User.objects.create(
            username='unittest_user',
            email='usertest@usertest.com',
            password='1q2w3e4r+',
            middle_name='Test Test'
        )

        cls.cart = create_cart(cls.user)
        cls.categories = create_categories_list()
        cls.products = create_products_list(cls.categories)
        print('cart', cls.cart)
        cls.seller = create_seller(cls.user)
        print('seller', cls.seller)
        cls.cart_items = create_cart_items(cls.products,
                                           cls.cart,
                                           cls.seller)
        print('cart_items', cls.cart_items)
        cls.order_data = {
            'user': cls.user.pk,
            'city': 'Test sity',
            'address': 'Test address 134',
            'email': 'usertest@usertest.com',
            'middle_name': 'Test Test',
            'phone': '+79148994101',
            'delivery_type': DeliveryType.REGULAR.name,
            'pay_type': PayType.bank_card.name,
            'amount': 1245.00
        }

    @classmethod
    def tearDownClass(cls) -> None:
        delete_products_list(cls.products)
        delete_categories_list(cls.categories)
        delete_cart_items(cls.cart_items)
        delete_seller(cls.seller)
        delete_cart(cls.cart)
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_create_order(self):

        response = self.client.post(
            reverse('order_app:create-order'),
            self.order_data
        )
        print(response)

        print('Order', Order.objects.filter(user=self.user))
        # self.assertTrue(
        #     Order.objects.filter(**self.order_data).exists()
        # )
        return True
