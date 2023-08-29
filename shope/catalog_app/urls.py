from django.urls import path
from .views import *


urlpatterns = [
    path('', TestCatalogView.as_view(), name="catalog"),
    path('comparison/', TestComparisonView.as_view(), name="comparison"),
    path('product/', TestProductView.as_view(), name="product"), #<int:product_id>/
    path('sale/', TestSaleView.as_view(), name="sale"),
    path('filter_catalog/', CatalogFilterView.as_view(), name="filter_catalog"),
]