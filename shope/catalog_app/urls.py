from django.urls import path
from django.views.decorators.cache import cache_page
from .views import (
    ProductDetailView,
    CatalogListView,
    TestComparisonView,
    SaleView,
    ProductSaleDetailView,
    ProductGroupSaleDetailView,
    AddProductToCartView,
    CartSaleDetailView,
    ChangeListProductViewedView, ProductViewedView
)

from core.utils.cache import get_cache_value

urlpatterns = [
    path('comparison/', TestComparisonView.as_view(), name="comparison"),
    path('product/<int:product_id>/', ProductDetailView.as_view(), name="product"),
    # path('product/<int:product_id>/', cache_page(get_cache_value('DETAIL_PRODUCT'))(ProductDetailView.as_view()), name="product"),
    path('changeviewedlist/<int:product_id>', ChangeListProductViewedView.as_view(), name='change_viewed'),
    path('viewed_products/<int:user_id>', ProductViewedView.as_view(), name='viewed_products'),
    path('sale/', SaleView.as_view(), name="sale"),

    path('catalog/', CatalogListView.as_view(), name="catalog"),
    path('catalog/add', AddProductToCartView.as_view(), name="catalog_add"),


    path('sale/<int:sale_id>/', ProductSaleDetailView.as_view(), name="product_sale_detail"),
    path('sale/<int:sale_id>/', ProductGroupSaleDetailView.as_view(), name="product_group_sale_detail"),
    path('sale/<int:sale_id>/', CartSaleDetailView.as_view(), name="cart_sale_detail"),

]
