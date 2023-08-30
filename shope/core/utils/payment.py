"""
Сервис интеграции с сервисом оплаты.
Ппозволяет:
 - оплатить заказ;
 - получить статус оплаты;
"""

from django.conf import settings

from yookassa import Configuration, Payment


class OrderPayment:
    """Класс интеграции с сервисом оплаты"""
    Configuration.account_id = settings.PAY_ACCOUNT_ID
    Configuration.secret_key = settings.PAY_ACCOUNT_SECRET_KEY

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
            "description": "Заказ №72"
        })

        return str(payment.confirmation.confirmation_token)
