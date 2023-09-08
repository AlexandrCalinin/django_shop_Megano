from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.generic import TemplateView, ListView

from catalog_app.models import Product
from repositories.cartitem_repositories import CartItemRepository
from repositories.cart_repositories import CartRepository

from .form import CartEditForm

from core.utils.add_product_to_cart import AddProductToCart


class CatalogView(ListView):
    template_name = 'catalog_app/catalog.html'
    context_object_name = 'products'
    queryset = Product.objects.prefetch_related('image')
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(CatalogView, self).get_context_data(**kwargs)

        cart = CartRepository()
        cartitem = CartItemRepository()

        cart_id = cart.get_by_user(_user_id=self.request.user.id)
        cartitem = cartitem.get_by_cart_id(_cart=cart_id)

        summ = 0
        count = 0
        for item in cartitem:
            summ += item.count
            count += item.amount

        context['count'] = count
        context['amount'] = summ

        return context

    def post(self, request, *args, **kwargs):

        if request.headers['X-Requested-With'] == 'XMLHttpRequest':
            form = CartEditForm(request.POST)
            if form.is_valid():
                add = AddProductToCart()
                summ, count = add.add_product_to_cart(form.cleaned_data, request.user.id)

                context = self.get_context_data(object_list=self.get_queryset(), **kwargs)

                context['count'] = count
                context['amount'] = summ

                result = render_to_string('includes/card_edit.html', context=context, request=request)
                return JsonResponse({'result': result})

class TestComparisonView(TemplateView):
    template_name = 'catalog_app/comparison.html'


class TestProductView(TemplateView):
    template_name = 'catalog_app/product.html'


class TestSaleView(TemplateView):
    template_name = 'catalog_app/sale.html'


class CatalogFilterView(TemplateView):
    template_name = 'catalog_app/filter_catalog.html'
