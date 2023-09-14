import inject
from core.utils.injector import configure_inject

from interface.cart_interface import ICart
from interface.cartitem_interface import ICartItem

from django.views.generic import ListView


configure_inject()


class CartView(ListView):
    template_name = 'cart_app/cart.html'
    context_object_name = "items"
    _cart: ICart = inject.attr(ICart)
    _cartitem: ICartItem = inject.attr(ICartItem)

    def get_queryset(self):
        cart = self._cart.get_by_user(_user=self.request.user)
        return self._cartitem.get_by_cart_id(_cart=cart)

    def get_context_data(self, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)

        cart = self._cart.get_by_user(_user=self.request.user)
        cart_products = self._cartitem.get_by_cart_id(_cart=cart)

        summ = 0
        count = 0
        for item in cart_products:
            count += item.count
            summ += item.amount

        context['count'] = count
        context['amount'] = summ

        return context
