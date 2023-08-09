from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import PasswordResetView, LogoutView
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView


class SetNewPasswordView(PasswordResetView):
    template_name = "auth/password.html"


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "auth/registr.html"


class ForgotPasswordView(View):
    template_name = "auth/e-mail.html"


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('auth_app:login')
