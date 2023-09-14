from core.utils.add_product_to_cart import AddProductToCart

from django.views.generic import ListView


class CartView(ListView):
    template_name = 'cart_app/cart.html'
    context_object_name = "items"

    def get_queryset(self):
        return AddProductToCart().get_list_in_cart(self.request.user)

    def get_context_data(self, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)
        summ, count = AddProductToCart().get_count_product_in_cart(self.request.user)
        context['amount'] = summ
        context['count'] = count

        return context
