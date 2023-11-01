import random
from django.test import TestCase
from django.urls import reverse
from django.utils import formats

from datetime import date

from catalog_app.models import Product

NUMBER_OF_SHOPS = 10


class TestBaseView(TestCase):

    fixtures = [
        '00_user.json',
        '01_category.json',
        '03_image.json',
        '05_tag.json',
        '07_taggeditem.json',
        '09_product.json',
        '11_seller.json',
        '12_price.json',
        '13_discount_product.json',
        '15_discount_product_group.json',
        '17_cart_sale.json',
        '19_banner.json',
        '21_slider.json',
        '22_characteristic_type.json',
        '23_characteristic_value.json',
        '24_characteristic_product.json',
    ]

    def test_base(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_count_top_products(self):
        url = reverse('home')
        response = self.client.get(url)
        for product in Product.objects.filter(is_active=False):
            self.assertContains(response, product.name)
