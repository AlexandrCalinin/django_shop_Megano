import inject
from django.views.generic import TemplateView

from core.utils.injector import configure_inject
from interface.banner_interface import IBanner
from interface.category_interface import ICategory
from interface.product_interface import IProduct
from interface.slider_interface import ISlider

configure_inject()


class BaseView(TemplateView):
    template_name = 'core/product_supply.html'
    _product_top_list: IProduct = inject.attr(IProduct)
    _category_list: ICategory = inject.attr(ICategory)
    _slider_list: ISlider = inject.attr(ISlider)
    _banner_list: IBanner = inject.attr(IBanner)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_top_list'] = self._product_top_list.get_product_top_list(const=8)
        context['category_list'] = self._category_list.get_category_list()
        context['slider_list'] = self._slider_list.get_slider_list(const=3)
        qs = self._banner_list.get_banner_list(const=3)
        for banner in qs:
            min_price = self._category_list.get_min_price_of_category(_category_id=banner.category.pk)
            self._banner_list.update_banner_price(_object=banner, _min_price=min_price)
        context['banner_list'] = qs
        return context


class AboutView(TemplateView):
    template_name = 'core/about.html'
    _category_list: ICategory = inject.attr(ICategory)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = self._category_list.get_category_list()
        return context
