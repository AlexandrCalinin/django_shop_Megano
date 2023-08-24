"""
Сервис интеграции с сервисом оплаты.
Ппозволяет:
 - оплатить заказ;
 - получить статус оплаты;
"""

from yookassa import Configuration, Payment


# для тестов, потом перенесу в .env
Configuration.account_id = '237093'
Configuration.secret_key = 'test_ggEVF9sH36dcZS6ahfZzaa0miBp4c-Y9IxJT4YTHS5k'


class OrderPayment:
    """Класс интеграции с сервисом оплаты"""

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
        print(payment.confirmation.confirmation_token)
        return str(payment.confirmation.confirmation_token)
