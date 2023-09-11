"""Forms for Profile app"""

from typing import Any, Dict
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.utils.translation import gettext_lazy as _
from phonenumber_field.formfields import PhoneNumberField
from .models import Profile
from auth_app.models import User


class EditUserForm(UserChangeForm):
    """Форма редактирования данных пользователя"""
    email = forms.EmailField(label=_('Email'),
                             widget=forms.EmailInput(attrs={'readonly': True}))

    middle_name = forms.CharField(label=_('Full name'),
                                  widget=forms.TextInput(attrs={'class': 'form-input', 'id': 'name'}))

    class Meta:
        """Meta Class"""
        model = User
        fields = [
            'email',
            'middle_name',
        ]


class EditProfileForm(forms.ModelForm):
    """Форма редактирования профайла пользователя"""
    phone = PhoneNumberField(label=_('Phone'),
                             widget=forms.TextInput(attrs={'class': 'form-input', 'id': 'phone'}))

    avatar = forms.ImageField(label=_('avatar'),
                              widget=forms.FileInput())

    class Meta:
        """Meta Class"""
        model = Profile
        fields = [
            'user',
            'phone',
            'avatar',
        ]
