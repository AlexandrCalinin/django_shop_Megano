from django.contrib.auth.views import LoginView
from django.urls import path
from .views import WebPasswordResetView, EmailView, RegisterView

urlpatterns = [
    path('restore_password/password', WebPasswordResetView.as_view(), name='restore_password'),
    path('login/', LoginView.as_view(template_name="auth/login.html"), name="login"),
    path("restore_password/e-mail/", EmailView.as_view(), name="e-mail"),
    path("register/", RegisterView.as_view(), name="register"),
]