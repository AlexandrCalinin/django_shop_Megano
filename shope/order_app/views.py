"""Order views"""

import inject
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from core.utils.injector import configure_inject
from interface.order_interface import IOrder
from interface.order_item_interface import IOrderItem
from order_app.models import Order

configure_inject()


class HistoryOrderView(LoginRequiredMixin, ListView):
    """Oreder list tempale class. Will be deleted"""
    template_name = 'order_app/historyorder.html'
    context_object_name = 'order_list'
    paginate_by = 3
    model = Order
    _order_list: IOrder = inject.attr(IOrder)

    def get_queryset(self):
        return self._order_list.get_list_by_user(self.request.user)


class DetailOrderView(DetailView):
    """Детальная страница заказа"""
    template_name = 'order_app/oneorder.html'
    model = Order
    context_object_name = 'order'
    _order: IOrder = inject.attr(IOrder)
    _order_item = inject.attr(IOrderItem)

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return self._order.get_by_pk(pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_items'] = self._order_item.get_by_order(self.get_object())
        return context


class CreateOrderView(TemplateView):
    """Oreder detail tempale class. Will be deleted"""
    template_name = 'order_app/order.html'
