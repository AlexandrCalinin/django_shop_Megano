from django.db import models
from django.utils.translation import gettext_lazy as _

from auth_app.models import User
from core.models import BaseModel


class Profile(BaseModel):
    """Модель профайла"""
    phone = models.CharField(max_length=10, verbose_name=_('Phone'))
    image = models.ImageField(upload_to="photos/%Y/%m/%d", verbose_name=_('Avatar'))
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('User'))

    def __str__(self):
        return self.user

    class Meta:
        verbose_name = _('User Profile')
        verbose_name_plural = _('User Profiles')
        ordering = ['id']
