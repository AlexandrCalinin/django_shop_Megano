from django.http import JsonResponse
from django.template.loader import render_to_string
from.form import ChangeCountForm
from core.utils.add_product_to_cart import AddProductToCart

from django.views.generic import ListView


class CartView(ListView):
    template_name = 'cart_app/cart.html'
    context_object_name = "items"

    def get_queryset(self):
        return AddProductToCart().get_list_in_cart(self.request)

    def post(self, request):
        if request.headers['X-Requested-With'] == 'XMLHttpRequest':
            form = ChangeCountForm(request.POST)
            add = AddProductToCart()

            if form.is_valid():
                if request.user.is_authenticated:
                    product_amount = add.change_count_product_in_cart(request.user, **form.cleaned_data)
                    amount, count = add.get_count_product_in_cart(user=request.user)
                else:
                    product_amount = add.change_count_product_in_cart_for_anonymous(request, **form.cleaned_data)
                    amount, count = add.get_count_product_for_anonymous_user(request)

                context = self.get_context_data(object_list=self.get_queryset())

                context["count"] = count
                context["amount"] = amount

                cart_edit = render_to_string('includes/card_edit.html', context=context, request=request)
                count_change = render_to_string('includes/price_product_in_cart.html', context={"product_amount": product_amount}, request=request)
                total_amount = render_to_string('includes/total_amount_in_cart.html', context=context, request=request)

                return JsonResponse({'cart': cart_edit, 'count_change': count_change, 'total_amount': total_amount})
