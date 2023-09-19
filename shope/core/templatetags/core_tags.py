"""Custom teplates tags"""


from django import template
from core.enums import PayType, DeliveryType, OrderStatus

register = template.Library()


@register.inclusion_tag('includes/order-information.html')
def get_order(order):
    """" Вывод информации по заказу """

    context = {
        'order': order,
        'delivery_type': DeliveryType[order.delivery_type],
        'pay_type': PayType[order.pay_type],
        'status': OrderStatus[order.status]
    }
    return context
