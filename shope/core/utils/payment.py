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

    def __init__(self, pk) -> None:
        """ Инициализация класса"""
        self.order = self._order.get_by_pk(pk)[0]
        self.value = self.order.amount
        self.order_pk = self.order.pk

    def new_order_pay(self):
        """
        Новая оплата по заказу.
        Тестовая реализация
        """

        payment = Payment.create({
            "amount": {
                "value": "2.00",
                "currency": "RUB"
            },
            "confirmation": {
                "type": "embedded"
            },
            "capture": True,
            "description": self.order_pk
        })

        self.order.payment_id = payment.id
        self._order.save(self.order)
        return str(payment.confirmation.confirmation_token)

    def pay_notifications(self):
        """Получить статус оплаты"""

        payment = Payment.find_one(self.order.payment_id)
        if payment.status == "succeeded":
            self.order.status = OrderStatus.PAID.name
            self._order.save(self.order)
            return True
        return False
