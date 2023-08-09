from django.contrib.auth.views import LoginView
from django.urls import path
from django.views.generic import TemplateView

from .views import WebPasswordResetView, EmailView, RegisterView, WebLogoutView

urlpatterns = [
    path('restore_password/', WebPasswordResetView.as_view(), name='restore_password'),
    path('login/', LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('e-mail/', EmailView.as_view(), name='e-mail'),
    path('register/', RegisterView.as_view(), name='register'),
    path('confirm-email/', TemplateView.as_view(template_name='auth/confirm-email.html'), name='confirm-email'),
    path('logout/', WebLogoutView.as_view(), name='logout'),
]