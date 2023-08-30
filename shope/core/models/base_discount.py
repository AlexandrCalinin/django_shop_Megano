from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .base_model import BaseModel


class DiscountBaseModel(BaseModel):
    """Базовая модель для скидок"""
    name = models.CharField(max_length=255, verbose_name=_('Discount name'))
    priority = models.PositiveIntegerField(default=1, verbose_name=_('Priority'))
    value = models.PositiveIntegerField(default=1, verbose_name=_('Sale value'))
    data_start = models.DateField(default=timezone.now, verbose_name=_('Date of discount start'))
    data_end = models.DateField(default=timezone.now, verbose_name=_('Date of discount end'))
    description = models.TextField(blank=True, verbose_name=_('Description'))

    class Meta:
        abstract = True
