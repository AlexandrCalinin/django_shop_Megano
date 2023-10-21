"""Тестирование catalog"""

from django.test import TestCase
from django.urls import reverse

from catalog_app.models import Product, Category


class ProfileTestCase(TestCase):
    """Тесты оплаты заказа"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.category = Category.objects.create(
            title='test category'
        )
        cls.product = Product.objects.create(
            title='test category',
            name='test category',
            category=cls.category
        )

    @classmethod
    def tearDownClass(cls) -> None:
        cls.product.delete()
        cls.category.delete()

    def test_detail_product_view(self):
        """Тест получение страницы профайла"""

        response = self.client.get(
            reverse('product', kwargs={'product_id': self.product.pk}),
        )
        context_data = response.context_data
        # проверяем, что нужная страница отркрылась
        self.assertEqual(response.status_code, 200)
        # проверяем, что загружен именно нш продукт
        self.assertEqual(context_data['product'], self.product)
