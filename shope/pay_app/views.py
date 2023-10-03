from django.shortcuts import render
from django.views.generic import TemplateView, View
from core.utils.payment import OrderPayment

from order_app.models import Order
import inject
from interface.order_interface import IOrder


class CreatePaymentView(View):
    """Оплатить заказ"""
    template_name = 'pay_app/new_payment.html'

    def get(self, request, pk):
        context = {'confirmation_t': OrderPayment(pk).new_order_pay(),
                   'pk': pk}

        return render(request, self.template_name, context)


class SaccessPaymentView(View):
    """Успешная оплата заказа."""
    template_name = 'pay_app/success.html'
    _order: IOrder = inject.attr(IOrder)

    def get(self, request, pk):
        OrderPayment(pk).pay_notifications()

        return render(request, self.template_name, {})
