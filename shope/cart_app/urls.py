from django.urls import path
from .views import CartListView, ChangeCountProductView, DeleteCartItemView, AddProductToCartView

app_name = 'cart_app'

urlpatterns = [
    path('cart', CartListView.as_view(), name="cart"),
    path('cart/change', ChangeCountProductView.as_view(), name="change_count"),
    path('cart/delete', DeleteCartItemView.as_view(), name="item_delete"),
    path('cart/add', AddProductToCartView.as_view(), name="catalog_add"),
]