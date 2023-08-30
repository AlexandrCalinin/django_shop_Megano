import inject

from django.conf import settings
from django.contrib import auth
from django.contrib.auth.views import PasswordResetView, LogoutView
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import FormView

from .models import User
from .forms import UserRegisterForm
from core.utils.injector import configure_inject
from interface.auth_interface import IAuth

configure_inject()


class SetNewPasswordView(PasswordResetView):
    template_name = "auth/password.html"


class RegisterView(FormView):
    _user: IAuth = inject.attr(IAuth)
    form_class = UserRegisterForm
    template_name = "auth/registr.html"
    success_url = reverse_lazy('auth_app:login')

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = form.save()
            if self.send_link_to_verify_email(self, user=user):
                return HttpResponseRedirect(reverse('auth_app:login'))
            else:
                print("Email is not verified")
        else:
            print("Form is not valid")
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    @staticmethod
    def send_link_to_verify_email(self, user):
        verify_link = reverse_lazy('auth_app:verify_email', args=[user.email, user.activation_key])
        subject = f'Для активации учетной записи {user.username} пройдите по ссылке'
        message = f'Для подтверждения учетной записи {user.username} перейдите по ссылке' \
                  f' на портале \n {settings.DOMAIN_NAME}{verify_link}'
        return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

    def verify(self, email, activate_key):
        try:
            user = self._user.get_user_by_email(_email=email)

            if user.activation_key == activate_key and not User.activation_key_expired(user):
                user.activation_key = ''
                user.is_activation_key_expired = None
                user.is_active = True
                user.save()
                auth.login(self, user)
            return reverse_lazy('home')

        except Exception:
            self._user.delete_user_by_email(email)
            return render(self, 'auth/registration-error.html')


class VerifyEmailView(View):
    template_name = 'auth/verify-email.html'

    def get(self, request, email, activate_key):
        return render(request, 'auth/verify-email.html')


class ForgotPasswordView(View):
    template_name = "auth/e-mail.html"


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('auth_app:login')
