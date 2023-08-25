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


class SetNewPasswordView(PasswordResetView):
    template_name = "auth/password.html"


class RegisterView(FormView):
    model = User
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
                  f' на портале \n http://127.0.0.1:8000/{verify_link}'
        return send_mail(subject, message, "AlexandrKalinin123@yandex.ru", [user.email], fail_silently=False)

    def verify(self, email, activate_key):
        try:
            user = User.objects.get(email=email)
            if user and user.activation_key == activate_key and not user.is_activation_key_expires():
                user.activation_key = ''
                user.activation_key_expires = None
                user.is_active = True
                user.save()
                auth.login(self, user)
            return render(self, 'auth/virify-email.html')
        except Exception:
            return HttpResponseRedirect(reverse('/'))


class EmailVerifyView(View):
    template_name = 'auth/verify_email.html'


class ForgotPasswordView(View):
    template_name = "auth/e-mail.html"


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('auth_app:login')
