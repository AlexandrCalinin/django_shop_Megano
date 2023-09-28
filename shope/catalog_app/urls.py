from django.urls import path
from .views import (
    ProductDetailView,
    CatalogListView,
    CatalogFilterView,
    TestComparisonView,
    SaleView,
    ProductSaleDetailView,
    ProductGroupSaleDetailView,
    CartSaleDetailView,
    AddProductToCartView,
)

urlpatterns = [
    path('comparison/', TestComparisonView.as_view(), name="comparison"),

    path('product/<int:pk>/', ProductDetailView.as_view(), name="product"),  # <int:product_id>/
    path('sale/', SaleView.as_view(), name="sale"),
    path('filter_catalog/', CatalogFilterView.as_view(), name="filter_catalog"),
    path('catalog/', CatalogListView.as_view(), name="catalog"),
    path('catalog/add', AddProductToCartView.as_view(), name="catalog_add"),


    path('sale/<int:sale_id>/', ProductSaleDetailView.as_view(), name="product_sale_detail"),
    path('sale/<int:sale_id>/', ProductGroupSaleDetailView.as_view(), name="product_group_sale_detail"),
    path('sale/<int:sale_id>/', CartSaleDetailView.as_view(), name="cart_sale_detail"),

]
