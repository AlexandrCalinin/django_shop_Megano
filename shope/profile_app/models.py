from django.db import models
from django.utils.translation import gettext_lazy as _

from auth_app.models import User
from core.models import BaseModel


class Profile(BaseModel):
    """Модель профайла"""
    phone = models.CharField(max_length=10, verbose_name=_('phone'))
    image = models.ImageField(upload_to="photos/%Y/%m/%d", verbose_name=_('avatar'))
    user = models.OneToOneField(User, blank=True, on_delete=models.CASCADE, verbose_name=_('user'))

    def __str__(self):
        return self.user

    class Meta:
        verbose_name = _('user profile')
        verbose_name_plural = _('user profiles')
        ordering = ['id']
