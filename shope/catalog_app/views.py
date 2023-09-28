"""Catalog app views"""
import inject

from django.http import HttpResponseRedirect
from django.views import View

from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic import TemplateView, ListView, DetailView
from django.db.models import Max, Count, Subquery, F, OuterRef

from core.utils.injector import configure_inject
from interface.cart_sale_interface import ICartSale
from interface.category_interface import ICategory
from interface.discount_product_group_interface import IDiscountProductGroup
from interface.discount_product_interface import IDiscountProduct
from interface.characteristic_interface import ICharacteristicProduct
from catalog_app.models import DiscountProduct, DiscountProductGroup, CartSale, ProductViewed
from catalog_app.models import Product

from interface.product_viewed_interface import IProductViewed

from interface.catalog_filter_interface import ICatalogFilter
from core.models.price import Price


configure_inject()


class ProductDetailView(DetailView):
    """Детальная страница продукта"""
    _characteristics: ICharacteristicProduct = inject.attr(ICharacteristicProduct)

    model = Product
    template_name = 'catalog_app/product.html'
    context_object_name = 'product'
    pk_url_kwarg = 'product_id'

    def get_queryset(self):
        """get querysert"""
        return Product.objects.prefetch_related(
            'image',
            'tag',
        )

    def get_context_data(self, **kwargs):
        """get_context_data"""
        contex = super().get_context_data(**kwargs)
        contex['characteristics'] = self._characteristics.get_by_product(_product=self.object)

        latest_prices = Product.objects.filter(pk=self.kwargs.get('product_id')).annotate(
            latest_price=Max('price__date')
        ).annotate(
            latest_price_value=Subquery(
                Price.objects.filter(
                    product=OuterRef('pk'),
                    date=F('product__price__date')
                ).values('price')[:1]
            )
        ).annotate(
            price_count=Count('price')
        ).filter(price_count__gt=0)

        for i_price in latest_prices:
            print(f'{i_price} - {i_price.latest_price_value}')
        return contex


class CatalogView(ListView):
    template_name = 'catalog_app/catalog.html'
    _filter: ICatalogFilter = inject.attr(ICatalogFilter)

    def get(self, request, **kwargs):
        return super().get(request, **kwargs)

    def get_queryset(self):
        try:
            if self.request.GET.get('tag') is not None:
                tag_name = self.request.GET.get('tag')
                return self._filter.filter_by_tag(tag_name)
            elif self.request.GET.get('sort') is not None:
                sort = self.request.GET.get('sort')
                return self._filter.filter_by_sort(sort)
            else:
                is_limited = True if self.request.GET.get('in_stock') else False
                free_delivery = True if self.request.GET.get('free_delivery') else False
                if self.request.GET.get('price'):
                    product_min_price, product_max_price = self.request.GET.get('price').split(';')
                else:
                    product_min_price, product_max_price = None, None
                product_name = self.request.GET.get('title')
                return self._filter.get_filtered_products(product_name, free_delivery,
                                                          is_limited, product_min_price, product_max_price)

        except MultiValueDictKeyError:
            return Product.objects.prefetch_related('image', 'tag')


class TestComparisonView(TemplateView):
    template_name = 'catalog_app/comparison.html'


class SaleView(TemplateView):
    template_name = 'catalog_app/sale.html'
    _product_sales: IDiscountProduct = inject.attr(IDiscountProduct)
    _product_group_sales: IDiscountProductGroup = inject.attr(IDiscountProductGroup)
    _cart_sales: ICartSale = inject.attr(ICartSale)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_sales'] = self._product_sales.get_list()
        context['product_group_sales'] = self._product_group_sales.get_list()
        context['cart_sales'] = self._cart_sales.get_list()
        return context


class ProductSaleDetailView(DetailView):
    template_name = 'catalog_app/sale_detail.html'
    model = DiscountProduct
    context_object_name = 'sale'
    pk_url_kwarg = 'sale_id'


class ProductGroupSaleDetailView(DetailView):
    template_name = 'catalog_app/sale_detail.html'
    model = DiscountProductGroup
    context_object_name = 'sale'
    pk_url_kwarg = 'sale_id'


class CartSaleDetailView(DetailView):
    template_name = 'catalog_app/sale_detail.html'
    model = CartSale
    context_object_name = 'sale'
    pk_url_kwarg = 'sale_id'


class ChangeListProductViewedView(View):
    """Представление для изменения списка просмотренных товаров"""
    _product_viewed_list: IProductViewed = inject.attr(IProductViewed)
    _create_product_viewed: IProductViewed = inject.attr(IProductViewed)
    _get_product_viewed_by_id: IProductViewed = inject.attr(IProductViewed)
    _delete_product_viewed_by_id: IProductViewed = inject.attr(IProductViewed)

    def post(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id')
        if request.user.is_authenticated:
            user_id = request.user.id
            product = self._get_product_viewed_by_id.get_product_viewed_by_id(_user_id=user_id, _product_id=product_id)
            if not product:
                self._create_product_viewed.create_product_viewed(_user_id=user_id, _product_id=product_id)
            else:
                self._delete_product_viewed_by_id.delete_product_viewed_by_id(_user_id=user_id, _product_id=product_id)
                self._create_product_viewed.create_product_viewed(_user_id=user_id, _product_id=product_id)
            product_viewed_list = self._product_viewed_list.get_product_viewed_list(_user_id=user_id)
            if len(product_viewed_list) > 20:
                self._delete_product_viewed_by_id.delete_product_viewed_by_id(
                    _user_id=product_viewed_list.first().user_id, _product_id=product_viewed_list.first().product_id)
        return HttpResponseRedirect(f'/catalog/product/{product_id}/')


class ProductViewedView(TemplateView):
    """Представление для отображения списка просмотренных товаров"""
    template_name = 'catalog_app/product_viewed.html'
    _category_list: ICategory = inject.attr(ICategory)
    _product_viewed_list: IProductViewed = inject.attr(IProductViewed)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.user.id
        context['product_viewed_list'] = self._product_viewed_list.get_product_viewed_list(_user_id=user_id)
        context['category_list'] = self._category_list.get_category_list()
        return context
