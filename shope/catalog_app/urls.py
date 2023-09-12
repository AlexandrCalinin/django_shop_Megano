from django.urls import path
from .views import (
    ProductDetailView,
    TestCatalogView,
    TestSaleView,
    CatalogFilterView,
    TestComparisonView

)


urlpatterns = [
    path('', TestCatalogView.as_view(), name="catalog"),
    path('comparison/', TestComparisonView.as_view(), name="comparison"),
    path('product/<int:pk>/', ProductDetailView.as_view(), name="product"),  # <int:product_id>/
    path('sale/', TestSaleView.as_view(), name="sale"),
    path('filter_catalog/', CatalogFilterView.as_view(), name="filter_catalog"),
]
