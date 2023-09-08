from django.forms import ModelForm

from cart_app.models import CartItem


class CartEditForm(ModelForm):
    class Meta:
        model = CartItem
        fields = ['product', 'count', 'amount']