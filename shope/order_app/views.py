"""Order views"""
import inject
from django.views.generic import TemplateView

from core.utils.injector import configure_inject
from interface.order_interface import IOrder
from order_app.models import Order

configure_inject()

class HistoryOrderView(TemplateView):
    """Oreder list tempale class. Will be deleted"""
    template_name = 'order_app/historyorder.html'


class OneOrderView(TemplateView):
    """Oreder detail tempale class. Will be deleted"""
    template_name = 'order_app/oneorder.html'

    _order:IOrder = inject.attr(IOrder)


    def get(self, request, *args, **kwargs):
        order = self._order.get_by_id(_id=request.id)

        order = Order.create(

        )

        self._order.save(model=order)


class CreateOrderView(TemplateView):
    """Oreder detail tempale class. Will be deleted"""
    template_name = 'order_app/order.html'
