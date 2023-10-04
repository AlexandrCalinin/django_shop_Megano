import hashlib
import random

from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm, AuthenticationForm, \
    UsernameField
from django import forms
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from .models import User


class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    username = forms.CharField(max_length=64, widget=forms.TextInput(attrs={'placeholder': 'Имя пользователя'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    first_name = forms.CharField(max_length=48, widget=forms.TextInput(attrs={'placeholder': 'Имя'}))
    last_name = forms.CharField(max_length=48, widget=forms.TextInput(attrs={'placeholder': 'Фамилия'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Повторите пароль'}))

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save()
        user.is_active = False
        salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:6]
        user.activation_key = hashlib.sha1((user.email + salt).encode('utf8')).hexdigest()
        user.save()
        return user


class UserLoginForm(AuthenticationForm):

    class Meta:
        fields = ('email', 'password')

    username = UsernameField(
        widget=forms.TextInput(
            attrs={"autofocus": True,
                   "placeholder": "e-mail"
                   })
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.
        PasswordInput(
            attrs={"autocomplete": "current-password",
                   "placeholder": "********"
                   })
    )


class ResetPasswordForm(PasswordResetForm):
    class Meta:
        fields = 'email'

    email = forms.EmailField(max_length=254, widget=forms.EmailInput(attrs={'placeholder': 'Введите email'}))

    @staticmethod
    def get_token(user):
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)
        return token


class SetNewPasswordForm(SetPasswordForm):
    class Meta:
        fields = ('new_password1', 'new_password2')

    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Повторите ввод пароля'}))
