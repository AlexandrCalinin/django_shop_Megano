from django.contrib.auth import authenticate, login
from django.contrib.auth.views import PasswordResetView, LogoutView
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.contrib.auth.tokens import default_token_generator as token_generator

from .models import User
from .forms import UserRegisterForm


class SetNewPasswordView(PasswordResetView):
    template_name = "auth/password.html"


class RegisterView(View):
    template_name = "auth/registr.html"

    def get(self, request):
        context = {
            'form': UserRegisterForm
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form_class = UserRegisterForm(request.POST)

        if form_class.is_valid():
            print(2)
            form_class.save()
            username = form_class.cleaned_data.get('name')
            email = form_class.cleaned_data.get('login')
            password = form_class.cleaned_data.get('pass')
            user = authenticate(username=username, email=email, password=password)
            self.send_link_to_verify_email(request, user)
            return redirect('confirm-email')
        context = {
            'form': form_class
        }
        return render(request, self.template_name, context)

    def send_link_to_verify_email(self, request, user):
        current_site = get_current_site(request)
        context = {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': token_generator.make_token(user),
        }
        message = render_to_string(template_name='auth/confirm-email.thml', context=context)
        email = EmailMessage(
            'Пожалуйста, перейдите на почту и подтвердите свой email для завершения регистрации',
            message,
            to=[user.email]
        )
        email.send()


class EmailVerifyView(View):
    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)

        if user is not None and token_generator.check_token(user, token):
            user.email_verify = True
            user.save()
            login(request, user)
            return redirect('/')
        return HttpResponse(_('Верификация почты не прошла'))

    @staticmethod
    def get_user(uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except Exception:
            user = None
        return user


class ForgotPasswordView(View):
    template_name = "auth/e-mail.html"


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('auth_app:login')
