
from django.views.generic import TemplateView, DetailView

from .models import Product


class ProductDetailView(DetailView):
    """Детальная страница продукта"""
    model = Product
    template_name = 'catalog_app/product.html'
    context_object_name = 'product'

    def get_queryset(self):
        """get querysert"""

        return Product.objects.prefetch_related(
            'image',
            'tag',
            'characteristic_product'
        )

    def get_context_data(self, **kwargs):
        """get_context_data"""
        contex = super().get_context_data(**kwargs)
        contex['characteristics'] = self.object.characteristic_product
        return contex


class TestCatalogView(TemplateView):
    template_name = 'catalog_app/catalog.html'


class TestComparisonView(TemplateView):
    template_name = 'catalog_app/comparison.html'


class TestSaleView(TemplateView):
    template_name = 'catalog_app/sale.html'


class CatalogFilterView(TemplateView):
    template_name = 'catalog_app/filter_catalog.html'
