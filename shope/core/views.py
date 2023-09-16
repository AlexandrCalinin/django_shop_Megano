import inject
from django.db.models import Sum, Q
from django.views.generic import TemplateView

from catalog_app.models import Product
from core.utils.injector import configure_inject
from interface.product_interface import IProduct

configure_inject()


class BaseView(TemplateView):
    template_name = 'core/product_supply.html'
    _product_top_list: IProduct = inject.attr(IProduct)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_is_authenticated'] = self.request.user.is_authenticated
        # qs = Product.objects.filter(orderitem__count__gte=1).annotate(qty=Sum('orderitem__count')).order_by('-qty')[:8]
        # for item in qs:
        #     print(item, item.qty)
        # if len(qs) < 8:
        #     qs_id = Product.objects.filter(~Q(id__in=qs))[:8-len(qs)]
        #     print('qs_id', qs_id)
        #
        # print('qs', len(list(qs) + list(qs_id)), list(qs) + list(qs_id))
        context['product_top_list'] = self._product_top_list.get_product_top_list(const=8)

        return context


class AboutView(TemplateView):
    template_name = 'core/about.html'
