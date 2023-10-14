"""Catalog app views"""

from django.http import JsonResponse, HttpRequest
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse

# кеширование
from django.core.cache import cache
import inject

from django.http import HttpResponseRedirect
from django.views import View

from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic import TemplateView, ListView, DetailView
from django.db.models import Max, Count, Subquery, F, OuterRef

from core.utils.injector import configure_inject
from interface.cart_sale_interface import ICartSale
from interface.category_interface import ICategory
from interface.product_interface import IProduct
from interface.discount_product_group_interface import IDiscountProductGroup
from interface.discount_product_interface import IDiscountProduct

from .form import CartEditForm

from core.utils.add_product_to_cart import AddProductToCart
from interface.characteristic_interface import ICharacteristicProduct
from catalog_app.models import DiscountProduct, DiscountProductGroup, CartSale
from catalog_app.models import Product

from interface.product_viewed_interface import IProductViewed

from interface.catalog_filter_interface import ICatalogFilter
from interface.seller_interface import ISeller
from interface.review_interface import IReview

from catalog_app.form import ReviewForm

from core.utils.cache import get_cache_value


configure_inject()


# def invalidate_cache(path='', *args, namespace=None):
#     request = HttpRequest()
#     request.META = {
#         'SERVER_NAME': '127.0.0.1',
#         'SERVER_PORT': 8000}
#     request.LANGUAGE_CODE = 'en-us'
#     if namespace:
#         path = namespace + ":" + path
#     request.path = reverse(path, args=args)

#     request.method = 'GET'

#     try:
#         cache_key = get_cache_key(request)
#         if cache_key:
#             if cache.has_key(cache_key):
#                 cache.delete(cache_key)
#                 return True
#             else:
#                 return False
#         else:
#             raise ValueError('failed to create cache_key')
#     except (ValueError, Exception) as e:
#         return False


class ProductDetailView(DetailView):
    """Детальная страница продукта"""
    _characteristics: ICharacteristicProduct = inject.attr(ICharacteristicProduct)
    _sellers_of_product: IProduct = inject.attr(IProduct)
    _price_of_seller: ISeller = inject.attr(ISeller)
    _review: IReview = inject.attr(IReview)

    model = Product
    template_name = 'catalog_app/product.html'
    context_object_name = 'product'
    pk_url_kwarg = 'product_id'

    def get_queryset(self):
        """get querysert"""
        key = 'PRODUCTS'
        qs = cache.get(key)
        if not qs:
            qs = Product.objects.all()
            cache.set(key, qs, get_cache_value('DETAIL_PRODUCT'))
        return qs

    def get_context_data(self, **kwargs):
        """get_context_data"""
        key = 'DETAIL_PRODUCT:' + str(self.kwargs['product_id'])
        cache_time = get_cache_value('DETAIL_PRODUCT')

        context = cache.get(key)

        if not context:
            context = {}
            context = super().get_context_data(**kwargs)
            context['characteristics'] = self._characteristics.get_by_product(_product=self.object)
            context['reviews'] = self._review.get_by_product(self.kwargs['product_id'])
            sellers = []
            min_price = {'price': 0,
                         'seller': None}
            for i_seller in self._sellers_of_product.get_sellers_of_product(self.kwargs['product_id']):
                price = self._price_of_seller.get_last_price_of_product(
                    i_seller['price__seller'],
                    self.kwargs['product_id']
                )
                sellers.append(price)
                if (price['product_seller__price'] < min_price['price']) or min_price['price'] == 0:
                    min_price['price'] = price['product_seller__price']
                    min_price['seller'] = price['pk']

            context['sellers'] = sellers
            context['min_price'] = min_price

            cache.set(key, context, cache_time)

        context['review_form'] = ReviewForm()
        context['cache_time'] = cache_time

        return context

    def post(self, request, product_id):
        """Метод post для добавление отзыва"""
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review_form.save()
            return redirect(self.request.path)

        context = {
            'review_form': review_form,
        }

        return render(request, self.template_name, context=context)


class CatalogListView(ListView):
    """Каталог"""
    template_name = 'catalog_app/catalog.html'
    _filter: ICatalogFilter = inject.attr(ICatalogFilter)

    def get(self, request, **kwargs):
        return super().get(request, **kwargs)

    def get_queryset(self):
        global query
        try:
            if self.request.GET.get('category') is not None:
                category_id = self.request.GET.get('category')
                query = self._filter.get_filtered_products_by_category(category_id)
            elif self.request.GET.get('char') is not None:
                char_id = self.request.GET.get('char')
                query = self._filter.get_filtered_products_by_char(char_id)
            elif self.request.GET.get('tag') is not None:
                tag_name = self.request.GET.get('tag')
                query = self._filter.filter_by_tag(tag_name)
            elif (self.request.GET.get('in_stock') or self.request.GET.get('free_delivery') or self.request.GET.get(
                    'price') or self.request.GET.get('title')):
                is_limited = True if self.request.GET.get('in_stock') else False
                free_delivery = True if self.request.GET.get('free_delivery') else False
                if self.request.GET.get('price'):
                    product_min_price, product_max_price = self.request.GET.get('price').split(';')
                else:
                    product_min_price, product_max_price = None, None
                product_name = self.request.GET.get('title')
                query = self._filter.get_filtered_products(product_name, free_delivery,
                                                           is_limited, product_min_price, product_max_price)
        except MultiValueDictKeyError:
            return Product.objects.prefetch_related('image', 'tag')
        finally:
            if self.request.GET.get('sort') is not None:
                sort = self.request.GET.get('sort')
                return self._filter.filter_by_sort(sort, query)
            else:
                return query


class AddProductToCartView(TemplateView):

    def post(self, request: HttpRequest):
        if request.headers['X-Requested-With'] == 'XMLHttpRequest':
            form = CartEditForm(data=request.POST)

            if form.is_valid():
                add = AddProductToCart()
                if request.user.is_authenticated:
                    add.add_product_to_cart(request.user, **form.cleaned_data, )
                else:
                    add.add_product_for_anonymous_user(request, **form.cleaned_data)

                result = render_to_string('includes/card_edit.html', request=request)
                return JsonResponse({'result': result})


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
