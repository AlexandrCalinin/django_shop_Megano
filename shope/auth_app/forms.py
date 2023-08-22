import hashlib
from random import random

from django.contrib.auth.forms import UserCreationForm

from .models import User


class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def __init__(self, *args, **kwargs):
        super(UserCreationForm).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['placeholder'] = 'Введите имя пользователя'
        self.email['email'].widget.attrs['placeholder'] = 'Введите email'
        self.password['password'].widget.attrs['placeholder'] = 'Введите пароль'

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save()
        user.is_active = False
        salt = hashlib.sha1(str(random()).encode('utf8')).hexdigest()[:6]
        user.activation_key = hashlib.sha1((user.email + salt).encode('utf8')).hexdigest()
        user.save()
        return user
