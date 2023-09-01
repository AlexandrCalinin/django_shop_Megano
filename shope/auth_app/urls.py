from django.urls import path
from django.views.generic import TemplateView

from .views import SetNewPasswordView, ForgotPasswordView, \
    RegisterView, UserLogoutView, VerifyEmailView, UserLoginView

app_name = 'auth_app'

urlpatterns = [
    path('set-new-password/<email>/<uidb64>/<token>/', SetNewPasswordView.as_view(), name='restore_password'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='e-mail'),
    path('register/', RegisterView.as_view(), name='register'),
    path('confirm-email/', TemplateView.as_view(template_name='auth/confirm-email.html'), name='confirm-email'),
    path('verify_email/<email>/<activate_key>/', VerifyEmailView.as_view(), name='verify_email'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
]
