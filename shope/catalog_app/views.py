"""Catalog app views"""
from django.http import JsonResponse
from django.template.loader import render_to_string

from core.models import Price

import inject
from django.views.generic import TemplateView, ListView, DetailView
from core.utils.injector import configure_inject
from interface.cart_sale_interface import ICartSale
from interface.discount_product_group_interface import IDiscountProductGroup
from interface.discount_product_interface import IDiscountProduct
from interface.cart_interface import ICart
from interface.cartitem_interface import ICartItem

from .form import CartEditForm

from core.utils.add_product_to_cart import AddProductToCart
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


class CatalogView(ListView):
    template_name = 'catalog_app/catalog.html'
    context_object_name = 'products'
    queryset = Price.objects.all()
    paginate_by = 10
    ordering = ['price']
    _cart: ICart = inject.attr(ICart)
    _cartitem: ICartItem = inject.attr(ICartItem)

    def get_context_data(self, **kwargs):
        context = super(CatalogView, self).get_context_data(**kwargs)

        try:
            summ, count = AddProductToCart().get_count_product_in_cart(user=self.request.user)
            context['count'] = count
            context['amount'] = summ
        except Exception:
            context['count'] = 0
            context['amount'] = 0
        return context

    def post(self, request, **kwargs):

        if request.headers['X-Requested-With'] == 'XMLHttpRequest':
            form = CartEditForm(request.POST)

            if form.is_valid():
                add = AddProductToCart()
                add.add_product_to_cart(form.cleaned_data, request.user)

                context = self.get_context_data(object_list=self.get_queryset(), **kwargs)

                summ, count = add.get_count_product_in_cart(request.user)
                context['count'] = count
                context['amount'] = summ

                result = render_to_string('includes/card_edit.html', context=context, request=request)
                return JsonResponse({'result': result})


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
