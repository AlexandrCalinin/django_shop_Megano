from django.views.generic import TemplateView


class TestCatalogView(TemplateView):
    template_name = 'catalog_app/catalog.html'


class TestComparisonView(TemplateView):
    template_name = 'catalog_app/comparison.html'


class TestProductView(TemplateView):
    template_name = 'catalog_app/product.html'


class TestSaleView(TemplateView):
    template_name = 'catalog_app/sale.html'


class CatalogFilterView(TemplateView):
    template_name = 'catalog_app/filter_catalog.html'
