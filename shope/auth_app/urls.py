from django.contrib.auth.views import LoginView
from django.urls import path
from django.views.generic import TemplateView

from .views import SetNewPasswordView, ForgotPasswordView, RegisterView, UserLogoutView, EmailVerifyView

app_name = 'auth_app'

urlpatterns = [
    path('set-new-password/', SetNewPasswordView.as_view(), name='restore_password'),
    path('login/', LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='e-mail'),
    path('register/', RegisterView.as_view(), name='register'),
    path('confirm-email/', TemplateView.as_view(template_name='auth/confirm-email.html'), name='confirm-email'),
    path('verify_email/<email>/<token>/', EmailVerifyView.as_view(), name='verify_email'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
]