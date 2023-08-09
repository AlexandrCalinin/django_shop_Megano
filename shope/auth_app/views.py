from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import PasswordResetView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView


class WebPasswordResetView(PasswordResetView):
    template_name = "auth/password.html"


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "auth/registr.html"


class EmailView(CreateView):
    template_name = "auth/e-mail"


class WebLogoutView(LogoutView):
    next_page = reverse_lazy('auth_app:login')
