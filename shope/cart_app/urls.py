from django.urls import path
from .views import TestView


urlpatterns = [
    path('test_cart.html', TestView.as_view(), name="test_cart.html")
]