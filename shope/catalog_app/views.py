from django.http import JsonResponse
from django.template.loader import render_to_string


from core.models import Price
from repositories.cartitem_repositories import CartItemRepository
from repositories.cart_repositories import CartRepository
import inject
from django.views.generic import TemplateView, ListView, DetailView

from catalog_app.models import DiscountProduct, DiscountProductGroup, CartSale

from core.utils.injector import configure_inject
from interface.discount_interface import IDiscountProduct, IDiscountProductGroup, ICartSale

configure_inject()

from .form import CartEditForm

from core.utils.add_product_to_cart import AddProductToCart


class CatalogView(ListView):
    template_name = 'catalog_app/catalog.html'
    context_object_name = 'products'
    queryset = Price.objects.all()
    paginate_by = 10
    ordering = ['price']

    def get_context_data(self, **kwargs):
        context = super(CatalogView, self).get_context_data(**kwargs)

        cart = CartRepository()
        cartitem = CartItemRepository()
        try:
            cart_id = cart.get_by_user(_user=self.request.user)
            cartitem = cartitem.get_by_cart_id(_cart=cart_id)

            summ = 0
            count = 0
            for item in cartitem:
                count += item.count
                summ += item.amount

            context['count'] = count
            context['amount'] = summ

        except Exception:
            context['count'] = 0
            context['amount'] = 0
        return context

    def post(self, request, *args, **kwargs):

        if request.headers['X-Requested-With'] == 'XMLHttpRequest':
            form = CartEditForm(request.POST)

            if form.is_valid():
                add = AddProductToCart()
                summ, count = add.add_product_to_cart(form.cleaned_data, request.user)

                context = self.get_context_data(object_list=self.get_queryset(), **kwargs)

                context['count'] = count
                context['amount'] = summ

                result = render_to_string('includes/card_edit.html', context=context, request=request)
                return JsonResponse({'result': result})


class TestComparisonView(TemplateView):
    template_name = 'catalog_app/comparison.html'


class TestProductView(TemplateView):
    template_name = 'catalog_app/product.html'


class SaleView(TemplateView):
    template_name = 'catalog_app/sale.html'
    _product_sales: IDiscountProduct = inject.attr(IDiscountProduct)
    _product_group_sales: IDiscountProductGroup = inject.attr(IDiscountProductGroup)
    _cart_sales: ICartSale = inject.attr(ICartSale)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_sales'] = self._product_sales.get_object_list(DiscountProduct)
        context['product_group_sales'] = self._product_group_sales.get_object_list(DiscountProductGroup)
        context['cart_sales'] = self._cart_sales.get_object_list(CartSale)
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
