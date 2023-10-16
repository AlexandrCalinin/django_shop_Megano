import datetime
import random
from django.shortcuts import render
import inject
from django.views.generic import TemplateView, View, UpdateView

from core.models.cache_setup import CacheSetup
from core.utils.cache import cache_values_list
from core.utils.injector import configure_inject
from interface.banner_interface import IBanner
from interface.product_interface import IProduct
from interface.slider_interface import ISlider


configure_inject()


class BaseView(TemplateView):
    template_name = 'core/product_supply.html'
    _products: IProduct = inject.attr(IProduct)
    _slider_list: ISlider = inject.attr(ISlider)
    _banner_list: IBanner = inject.attr(IBanner)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_top_list'] = self._products.get_product_top_list(const=8)
        context['product_limited_list'] = list(self._products.get_product_limit_list(const=17))
        context['offer_day'] = context['product_limited_list'].pop(random.randint(
            0, len(context['product_limited_list']) - 1))
        context['tomorrow_day'] = (datetime.date.today() + datetime.timedelta(days=2)).strftime('%d.%m.%Y')
        context['slider_list'] = self._slider_list.get_slider_list(const=3)
        context['banner_list'] = self._banner_list.get_banner_list(const=3)
        return context


class AboutView(TemplateView):
    template_name = 'core/about.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SetupAdminView(View):
    """Страница административных настроек"""
    template_name = 'core/setup-admin.html'

    def get(self, request, **kwargs):
        """Get"""
        context = {
            'cache_data': cache_values_list(),
        }
        return render(request, self.template_name, context)


class CacheUpdateView(UpdateView):
    """Обновление данных кеша"""
    model = CacheSetup
    fields = ['value']
    template_name = 'core/cache_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["key"] = self.object.key
        return context
