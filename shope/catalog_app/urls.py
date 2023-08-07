from django.urls import path
from .views import *


urlpatterns = [
    path('test_catalog', TestCatalogView.as_view(), name="test_catalog"),
    path('test_comparison', TestComparisonView.as_view(), name="test_comparison"),
    path('test_product', TestProductView.as_view(), name="test_product"),
    path('test_sale', TestSaleView.as_view(), name="test_sale"),
]