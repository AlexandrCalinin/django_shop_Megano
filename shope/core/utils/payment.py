"""
Сервис интеграции с сервисом оплаты.
Ппозволяет:
 - оплатить заказ;
 - получить статус оплаты;
"""

import os
from dotenv import load_dotenv, find_dotenv

from yookassa import Configuration, Payment

load_dotenv(find_dotenv())
PAY_ACCOUNT_ID = os.environ.get('PAY_ACCOUNT_ID')
PAY_ACCOUNT_SECRET_KEY = os.environ.get('PAY_ACCOUNT_SECRET_KEY')

Configuration.account_id = PAY_ACCOUNT_ID
Configuration.secret_key = PAY_ACCOUNT_SECRET_KEY


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
