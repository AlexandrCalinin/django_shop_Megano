from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.utils.translation import gettext_lazy as _

from .models import User


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    username = forms.CharField(
        label=_("username"),
        max_length=64
    )
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
    )
    password = forms.CharField(widget=forms.PasswordInput)

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save()
        user.is_active = False
        return user.save()
