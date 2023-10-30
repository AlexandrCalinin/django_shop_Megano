import random
from django.test import TestCase
from django.urls import reverse
from django.utils import formats

from datetime import date


NUMBER_OF_SHOPS = 10


class TestBaseView(TestCase):

    def test_base(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
