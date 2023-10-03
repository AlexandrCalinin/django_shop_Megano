from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.generic import ListView, TemplateView

from .form import ChangeCountForm, DeleteForm
from core.utils.add_product_to_cart import AddProductToCart


class CartListView(ListView):
    template_name = 'cart_app/cart.html'
    context_object_name = "items"

    def get_queryset(self):
        return AddProductToCart().get_list_in_cart(self.request)


class ChangeCountProductView(TemplateView):

    def post(self, request):
        if request.headers['X-Requested-With'] == 'XMLHttpRequest':

            form = ChangeCountForm(request.POST)
            add_product_to_cart = AddProductToCart()

            if form.is_valid():
                if request.user.is_authenticated:
                    product_amount = add_product_to_cart.change_count_product_in_cart(request.user, **form.cleaned_data)
                else:
                    product_amount = add_product_to_cart.change_count_for_anonymous(request, **form.cleaned_data)

                cart_edit = render_to_string('includes/card_edit.html',
                                             request=request)

                count_change = render_to_string('includes/price_product_in_cart.html',
                                                context={'item': product_amount},
                                               request=request)

                total_amount = render_to_string('includes/total_amount_in_cart.html', request=request)

                return JsonResponse({'cart': cart_edit,
                                     'count_change': count_change,
                                     'total_amount': total_amount})


class DeleteCartItemView(TemplateView):
    def post(self, request):
        form = DeleteForm(request.POST)
        if form.is_valid():
            add_product_to_cart = AddProductToCart()
            add_product_to_cart.remove_product_from_cart(form.cleaned_data['product'], self.request)

            cart_edit = render_to_string('includes/card_edit.html',
                                         request=request)

            total_amount = render_to_string('includes/total_amount_in_cart.html',
                                            request=request)

            return JsonResponse({'cart': cart_edit,
                                 'total_amount': total_amount})
