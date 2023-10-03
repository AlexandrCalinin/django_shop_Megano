"""
Сервис интеграции с сервисом оплаты.
Ппозволяет:
 - оплатить заказ;
 - получить статус оплаты;
"""

from django.conf import settings
from yookassa import Configuration, Payment
import inject
from interface.order_interface import IOrder
from core.enums import OrderStatus


class OrderPayment:
    """Класс интеграции с сервисом оплаты"""
    Configuration.account_id = settings.PAY_ACCOUNT_ID
    Configuration.secret_key = settings.PAY_ACCOUNT_SECRET_KEY
    _order: IOrder = inject.attr(IOrder)

    # def __init__(self, pk) -> None:
    #     """ Инициализация класса"""
    #     self.order = self._order.get_by_pk(pk)[0]
    #     self.value = self.order.amount
    #     self.order_pk = self.order.pk

    def new_order_pay(self, pk):
        """Новая оплата по заказу."""

        order = self._order.get_by_pk(pk)[0]

        payment = Payment.create({
            "amount": {
                "value": "2.00",
                "currency": "RUB"
            },
            "confirmation": {
                "type": "embedded"
            },
            "capture": True,
            "description": order.pk
        })

        order.payment_id = payment.id
        self._order.save(order)
        return str(payment.confirmation.confirmation_token)

    def pay_notifications(self, pk):
        """Получить статус оплаты методом GET"""
        order = self._order.get_by_pk(pk)[0]

        payment = Payment.find_one(order.payment_id)
        if payment.status == "succeeded":
            order.status = OrderStatus.PAID.name
            self._order.save(order)
            return True
        return False

    def pay_api_notifications(self, responce):
        """Получить статус оплаты API"""

        payment_id = responce['object']['id']
        order = self._order.get_by_payment_id(payment_id)
        if responce['object']['status'] == "succeeded":
            order.status = OrderStatus.PAID.name
            self._order.save(order)
            return True
        return False
