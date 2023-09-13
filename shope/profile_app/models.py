"""Profile app models"""

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField

from core.models import BaseModel


def profile_image_path(instance: "Profile", filename: str) -> str:
    """Путь к аватару профайла"""

    return f"profiles/profile_{instance.pk}/avatar/{filename}"


class Profile(BaseModel):
    """Модель профайла"""

    phone = PhoneNumberField(unique=True,
                             verbose_name=_('phone'),
                             blank=True,
                             null=True)

    avatar = models.ImageField(null=True,
                               blank=True,
                               verbose_name=_('avatar'),
                               upload_to=profile_image_path)  # type: ignore

    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                blank=True,
                                on_delete=models.CASCADE,
                                verbose_name=_('user'))

    def __str__(self):
        """Profile string"""
        return str(self.user)

    class Meta:
        """Meta class"""
        verbose_name = _("user's profile")
        verbose_name_plural = _("user's profiles")
        ordering = ['id']
