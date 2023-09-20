"""Catalog app views"""
import inject

from django.http import HttpResponseRedirect
from django.views import View

from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic import TemplateView, ListView, DetailView

from core.utils.injector import configure_inject
from interface.cart_sale_interface import ICartSale
from interface.category_interface import ICategory
from interface.discount_product_group_interface import IDiscountProductGroup
from interface.discount_product_interface import IDiscountProduct
from interface.characteristic_interface import ICharacteristicProduct
from catalog_app.models import DiscountProduct, DiscountProductGroup, CartSale, ProductViewed
from catalog_app.models import Product

from interface.product_viewed_interface import IProductViewed

from interface.catalog_filter_interface import ICatalogFilter


configure_inject()


class ProductDetailView(DetailView):
    """Детальная страница продукта"""
    _characteristics: ICharacteristicProduct = inject.attr(ICharacteristicProduct)

    model = Product
    template_name = 'catalog_app/product.html'
    context_object_name = 'product'
    pk_url_kwarg = 'product_id'

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
    _filter: ICatalogFilter = inject.attr(ICatalogFilter)

    def get(self, request, **kwargs):
        return super().get(request, **kwargs)

    def get_queryset(self):
        try:
            is_limited = True if self.request.GET.get('in_stock') else False
            free_delivery = True if self.request.GET.get('free_delivery') else False
            # range_price = self.request.GET.get('price')
            product_name = self.request.GET.get('title')
            queryset = self._filter.get_filtered_products(product_name, free_delivery, is_limited)
            return queryset

        except MultiValueDictKeyError:
            queryset = Product.objects.prefetch_related('image', 'tag')
            return queryset


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


class ChangeListProductViewedView(View):
    """Представление для изменения списка просмотренных товаров"""
    _product_viewed_list: IProductViewed = inject.attr(IProductViewed)

    def post(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id')
        if request.user.is_authenticated:
            user_id = request.user.id
            product, created = ProductViewed.objects.get_or_create(user_id=user_id, product_id=product_id)
            if not created:
                product.delete()
                ProductViewed.objects.create(user_id=user_id, product_id=product_id)
            product_viewed_list = self._product_viewed_list.get_product_viewed_list(_user_id=user_id)
            if len(product_viewed_list) > 20:
                product_viewed_list.first().delete()
        return HttpResponseRedirect(f'/catalog/product/{product_id}/')


class ProductViewedView(TemplateView):
    """Представление для отображения списка просмотренных товаров"""
    template_name = 'catalog_app/product_viewed.html'
    _category_list: ICategory = inject.attr(ICategory)
    _product_viewed_list: IProductViewed = inject.attr(IProductViewed)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.user.id
        context['product_viewed_list'] = self._product_viewed_list.get_product_viewed_list(_user_id=user_id)
        context['category_list'] = self._category_list.get_category_list()
        return context
