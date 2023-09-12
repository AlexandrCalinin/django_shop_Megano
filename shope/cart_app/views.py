
from django.views.generic import TemplateView


from repositories.cart_repositories import CartRepository
from repositories.cartitem_repositories import CartItemRepository


class CartView(TemplateView):
    template_name = 'cart_app/cart.html'

    def get_context_data(self, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)

        cart = CartRepository()
        cartitem = CartItemRepository()

        cart_id = cart.get_by_user(_user=self.request.user)
        cart_products = cartitem.get_by_cart_id(_cart=cart_id)

        summ = 0
        count = 0
        for item in cart_products:
            count += item.count
            summ += item.amount

        context['items'] = cart_products
        context['count'] = count
        context['amount'] = summ

        return context
