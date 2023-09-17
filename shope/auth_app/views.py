import inject

from django.conf import settings
from django.contrib.auth.views import PasswordResetView, LogoutView, PasswordResetConfirmView, LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic import FormView

from .forms import UserRegisterForm, ResetPasswordForm, SetNewPasswordForm, UserLoginForm
from core.utils.injector import configure_inject
from interface.auth_interface import IAuth
from .tasks import send_mail_to_user
from .models import User

configure_inject()


class RegisterView(FormView):
    form_class = UserRegisterForm
    _user: IAuth = inject.attr(IAuth)
    template_name = "auth_app/registr.html"
    success_url = reverse_lazy('auth_app:login')

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        email = request.POST['email']
        if form.is_valid():
            user = form.save()
            if self.send_link_to_verify_email(user=user):
                return HttpResponseRedirect(reverse('auth_app:confirm-email'))
            else:
                self._user.delete_user_by_email(_email=email)
        self._user.delete_user_by_email(_email=email)

        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    @staticmethod
    def send_link_to_verify_email(user):
        verify_link = reverse_lazy('auth_app:verify_email', args=[user.email, user.activation_key])
        subject = f'Для активации учетной записи {user.username} пройдите по ссылке'
        message = f'Для подтверждения учетной записи {user.username} перейдите по ссылке' \
                  f' на портале \n {settings.DOMAIN_NAME}{verify_link}'
        return send_mail_to_user.delay(subject, message, user.email)

    def verify(self, email, activate_key):
        try:
            user = User.objects.get(email=email)

            if user.activation_key == activate_key and not User.activation_key_expired(user):
                user.activation_key = ''
                user.is_activation_key_expired = None
                user.is_active = True
                user.save()
                auth.login(self, user)
            return HttpResponseRedirect(reverse('auth_app:login'))

        except Exception:
            User.objects.get(email).delete()
            return render(self, 'auth_app/registration-error.html')


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'auth_app/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form: UserLoginForm):
        """
        Метод, вызываемый при валидации формы
        """
        super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())


class ForgotPasswordView(SuccessMessageMixin, PasswordResetView):
    form_class = ResetPasswordForm
    _user: IAuth = inject.attr(IAuth)
    template_name = "auth_app/e-mail.html"
    success_url = reverse_lazy('home')

    def post(self, request, *args, **kwargs):
        try:
            form = self.form_class(data=request.POST)
            if form.is_valid():
                email = form.cleaned_data.get('email')
                user = self._user.get_user_by_email(_email=email)
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                token = form.get_token(user)
                if self.data_to_send_email(email=email, uidb64=uidb64, token=token, username=user.username):
                    return HttpResponseRedirect(reverse('auth_app:check_email_for_password_restore'))
                else:
                    raise Exception
        except Exception:
            return render(request, 'auth_app/change_password_error.html')

    @staticmethod
    def data_to_send_email(email, uidb64, token, username):
        subject = f'Для продолжения сброса пароля {username} пройдите по ссылке'
        message = f'Для подтверждения сброса пароля {username} перейдите по ссылке ' \
                  f'на портале \n{settings.DOMAIN_NAME}/auth/set-new-password/{uidb64}/{token}'
        return send_mail_to_user.delay(subject, message, email)


class SetNewPasswordView(SuccessMessageMixin, PasswordResetConfirmView):
    form_class = SetNewPasswordForm
    template_name = "auth_app/password_reset.html"
    success_url = reverse_lazy('auth_app:login')
    success_message = 'Пароль успешно изменен. Можете авторизоваться на сайте.'


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('auth_app:login')
