from django.urls import path
from .views import WebPasswordResetView

urlpatterns = [
    path('restore_password/', WebPasswordResetView.as_view(), name='restore_password'),
]