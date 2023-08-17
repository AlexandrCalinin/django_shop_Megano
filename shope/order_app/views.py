"""Order views"""

from django.views.generic import TemplateView


class HistoryOrderView(TemplateView):
    """Oreder list tempale class. Will be deleted"""
    template_name = 'order_app/historyorder.html'


class OneOrderView(TemplateView):
    """Oreder detail tempale class. Will be deleted"""
    template_name = 'order_app/oneorder.html'


class CreateOrderView(TemplateView):
    """Oreder detail tempale class. Will be deleted"""
    template_name = 'order_app/order.html'
