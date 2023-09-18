"""Order views"""
from typing import Any
from django.db.models.query import QuerySet
import inject
from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from core.utils.injector import configure_inject
from interface.order_interface import IOrder
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


class OneOrderView(TemplateView):
    """Oreder detail tempale class. Will be deleted"""
    template_name = 'order_app/oneorder.html'

    _order: IOrder = inject.attr(IOrder)

    def get(self, request, *args, **kwargs):
        order = self._order.get_by_id(_id=request.id)

        # order = Order.create(

        # )

        self._order.save(model=order)


class CreateOrderView(TemplateView):
    """Oreder detail tempale class. Will be deleted"""
    template_name = 'order_app/order.html'
