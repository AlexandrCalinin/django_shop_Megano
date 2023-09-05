"""Forms for Profile app"""

from django import forms
from django.utils.translation import gettext_lazy as _
from phonenumber_field.formfields import PhoneNumberField
from .models import Profile


class EditProfileForm(forms.ModelForm):
    """Форма редактирования профайла пользователя"""
    phone = PhoneNumberField(label=_('phone'))
    avatar = forms.ImageField(label=_('avatar'))

    class Meta:
        """Meta Class"""
        model = Profile
        fields = [
            'phone',
            'avatar',
        ]
