from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from cart_app.models import CartItem, Cart


class CartView(TemplateView):
    template_name = 'cart_app/cart.html'

    def get_context_data(self, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)
        cart_id = Cart.objects.get(user=self.request.user)
        cartitem = CartItem.objects.filter(cart_id=cart_id)
        context['items'] = cartitem
        return context
