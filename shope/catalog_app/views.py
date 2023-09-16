"""Catalog app views"""
import inject
from django.views.generic import TemplateView, ListView, DetailView

from core.utils.injector import configure_inject
from interface.cart_sale_interface import ICartSale
from interface.discount_product_group_interface import IDiscountProductGroup
from interface.discount_product_interface import IDiscountProduct
from interface.characteristic_interface import ICharacteristicProduct
from catalog_app.models import DiscountProduct, DiscountProductGroup, CartSale
from catalog_app.models import Product

configure_inject()


class ProductDetailView(DetailView):
    """Детальная страница продукта"""
    _characteristics: ICharacteristicProduct = inject.attr(ICharacteristicProduct)

    model = Product
    template_name = 'catalog_app/product.html'
    context_object_name = 'product'

    def get_queryset(self):
        """get querysert"""

        return Product.objects.prefetch_related(
            'image',
            'tag',
        )

    def get_context_data(self, **kwargs):
        """get_context_data"""
        contex = super().get_context_data(**kwargs)
        contex['characteristics'] = self._characteristics.get_by_product(_product=self.object)
        return contex


class TestCatalogView(ListView):
    template_name = 'catalog_app/catalog.html'
    queryset = Product.objects.prefetch_related('image', 'tag')


class TestComparisonView(TemplateView):
    template_name = 'catalog_app/comparison.html'


class SaleView(TemplateView):
    template_name = 'catalog_app/sale.html'
    _product_sales: IDiscountProduct = inject.attr(IDiscountProduct)
    _product_group_sales: IDiscountProductGroup = inject.attr(IDiscountProductGroup)
    _cart_sales: ICartSale = inject.attr(ICartSale)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_sales'] = self._product_sales.get_list()
        context['product_group_sales'] = self._product_group_sales.get_list()
        context['cart_sales'] = self._cart_sales.get_list()
        return context


class CatalogFilterView(TemplateView):
    template_name = 'catalog_app/filter_catalog.html'


class ProductSaleDetailView(DetailView):
    template_name = 'catalog_app/sale_detail.html'
    model = DiscountProduct
    context_object_name = 'sale'
    pk_url_kwarg = 'sale_id'


class ProductGroupSaleDetailView(DetailView):
    template_name = 'catalog_app/sale_detail.html'
    model = DiscountProductGroup
    context_object_name = 'sale'
    pk_url_kwarg = 'sale_id'


class CartSaleDetailView(DetailView):
    template_name = 'catalog_app/sale_detail.html'
    model = CartSale
    context_object_name = 'sale'
    pk_url_kwarg = 'sale_id'
