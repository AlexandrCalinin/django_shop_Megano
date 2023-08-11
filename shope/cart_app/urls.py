from django.urls import path
from .views import TestView


urlpatterns = [
    path('cart', TestView.as_view(), name="cart.")
]