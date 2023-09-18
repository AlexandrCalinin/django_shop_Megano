import inject
from django.views.generic import TemplateView

from core.utils.injector import configure_inject
from interface.product_interface import IProduct

configure_inject()


class BaseView(TemplateView):
    template_name = 'core/product_supply.html'
    _product_top_list: IProduct = inject.attr(IProduct)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_is_authenticated'] = self.request.user.is_authenticated
        context['product_top_list'] = self._product_top_list.get_product_top_list(const=8)

        return context


class AboutView(TemplateView):
    template_name = 'core/about.html'
