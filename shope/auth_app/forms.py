import hashlib
import random

from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm
from django import forms

from .models import User


class UserRegisterForm(UserCreationForm):
    # username = forms.CharField(label='username', max_length=64)
    # email = forms.EmailField(label='Email', max_length=200, widget=forms.EmailInput(attrs={'autocomplete': 'email'}))
    # first_name = forms.CharField(label='first_name', max_length=64)
    # last_name = forms.CharField(label='last_name', max_length=64)
    # password1 = forms.CharField(label='password1', max_length=20)
    # password2 = forms.CharField(label='password2', max_length=20)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def init(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Введите имя пользователя'
        self.fields['email'].widget.attrs['placeholder'] = 'Введите адрес эл.почты'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Введите  имя'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Введите  фамилию'
        self.fields['password1'].widget.attrs['placeholder'] = 'Введите пароль'
        self.fields['password2'].widget.attrs['placeholder'] = 'Повторите пароль'
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save()
        user.is_active = False
        salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:6]
        user.activation_key = hashlib.sha1((user.email + salt).encode('utf8')).hexdigest()
        user.save()
        return user


class ResetPasswordForm(PasswordResetForm):
    class Meta:
        fields = 'email'

    def init(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'Введите email'
        self.fields.widget.attrs['class'] = 'form-control py-4'


class SetNewPasswordForm(SetPasswordForm):
    class Meta:
        fields = ('new_password1', 'new_password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs['placeholder'] = 'Введите новый пароль'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Повторите ввод нового пароля'
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })
