from django.db import models
from .base_model import BaseModel
from django.utils.translation import gettext_lazy as _


class CacheSetup(BaseModel):
    """Модель административных настроек"""

    key = models.CharField(max_length=15, verbose_name=_('cache key'))

    value = models.PositiveIntegerField(default=86400,
                                        verbose_name=_('cache value'))
