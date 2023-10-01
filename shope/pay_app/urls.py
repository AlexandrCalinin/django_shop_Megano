"""Pay app urls"""

from django.urls import path
from .views import CreatePaymentView


app_name = 'pay_app'

urlpatterns = [
    path('new-pay/', CreatePaymentView.as_view(), name='new-pay'),
]
