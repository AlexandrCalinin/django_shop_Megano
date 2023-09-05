import inject

from django.conf import settings
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import PasswordResetView, LogoutView, PasswordResetConfirmView, LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import FormView

from .models import User
from .forms import UserRegisterForm, ResetPasswordForm, SetNewPasswordForm, UserLoginForm
from core.utils.injector import configure_inject
from interface.auth_interface import IAuth

configure_inject()


class RegisterView(FormView):
    _user: IAuth = inject.attr(IAuth)
    form_class = UserRegisterForm
    template_name = "auth_app/registr.html"
    success_url = reverse_lazy('auth_app:login')

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = form.save()
            if self.send_link_to_verify_email(user=user):
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
    def send_link_to_verify_email(user):
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
            return render(self, 'auth_app/registration-error.html')


class VerifyEmailView(View):
    template_name = 'auth_app/verify-email.html'

    def get(self, request, email, activate_key):
        return render(request, 'auth_app/verify-email.html')


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

    # def post(self, request, *args, **kwargs):
    #     if request.method == 'POST':
    #         form = UserLoginForm(data=request.POST)
    #         if form.is_valid():
    #             email = form.cleaned_data.get('email')
    #             password = form.cleaned_data.get('password')
    #             print(email)
    #             print(password)
    #             user = authenticate(request, email=email, password=password)
    #             if user is not None:
    #                 if user.is_active:
    #                     login(request, user)
    #                     return HttpResponse('Authenticated successfully')
    #                 else:
    #                     return HttpResponse('Disabled account')
    #             else:
    #                 return HttpResponse('Invalid email')
    #     else:
    #         form = UserLoginForm()
    #     return render(request, 'auth/login.html', {'form': form})


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
                if self.data_to_send_email(email=email, user=user):
                    return render(request, 'auth_app/change_password_success.html')
                else:
                    raise Exception
        except Exception:
            return render(request, 'auth_app/change_password_error.html')

    @staticmethod
    def data_to_send_email(email, user):
        subject = f'Для продолжения сброса пароля {user.username} пройдите по ссылке'
        message = f'Для подтверждения сброса пароля {user.username} перейдите по ссылке ' \
                  f'на портале \n{settings.DOMAIN_NAME}/auth_app/set-new-password/{email}'
        return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


class SetNewPasswordView(SuccessMessageMixin, PasswordResetConfirmView):
    form_class = SetNewPasswordForm
    _user: IAuth = inject.attr(IAuth)
    template_name = "auth_app/password.html"
    success_url = reverse_lazy('auth_app:login')
    success_message = 'Пароль успешно изменен. Можете авторизоваться на сайте.'

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            print(1)


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('auth_app:login')
