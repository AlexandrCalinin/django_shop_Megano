from django.shortcuts import render
from django.views.generic import TemplateView
from core.utils.payment import OrderPayment


class CreatePaymentView(TemplateView):
    """CreatePaymentView."""
    template_name = 'pay_app/new_payment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['confirmation_t'] = OrderPayment().new_order_pay()

        return context
