from django.urls import path
from django.views.decorators.cache import never_cache
from .views import CartListView, ChangeCountProductView, DeleteCartItemView

app_name = 'cart_app'

urlpatterns = [
    path('cart', never_cache(CartListView.as_view()), name="cart"),
    path('cart/change', never_cache(ChangeCountProductView.as_view()), name="change_count"),
    path('cart/delete', DeleteCartItemView.as_view(), name="item_delete"),
]
