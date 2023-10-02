"""Pay app urls"""

from django.urls import path
from .views import CreatePaymentView, SaccessPaymentView


app_name = 'pay_app'

urlpatterns = [
    path('new-pay/<int:pk>/', CreatePaymentView.as_view(), name='new-pay'),
    path('success-pay/<int:pk>', SaccessPaymentView.as_view(), name='success-pay'),
]
