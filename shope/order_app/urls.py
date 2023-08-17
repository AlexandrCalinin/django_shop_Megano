"""Order app urls"""

from django.urls import path
from .views import (HistoryOrderView,
                    OneOrderView,
                    CreateOrderView)


app_name = 'order_app'

urlpatterns = [
    path('history-order/', HistoryOrderView.as_view(), name='history-order'),
    path('one-order/', OneOrderView.as_view(), name='one-order'),
    path('create-order/', CreateOrderView.as_view(), name='create-order'),
]
