from django.db import models
from core.models.base_model import BaseModel
from django.utils.translation import gettext_lazy as _


class AdminSetup(BaseModel):
    """Модель административных настроек"""

    base_cache_time = models.PositiveIntegerField(default=86400,
                                                  verbose_name=_('base cache time (sec)'))

    category_cache_time = models.PositiveIntegerField(default=1800,
                                                      verbose_name=_('category cache time (sec)'),
                                                      help_text='default 30 min')

    banner_cache_time = models.PositiveIntegerField(default=600,
                                                    verbose_name=_('banner cache time (sec)'),
                                                    help_text='default 10 min')

    catalog_cache_time = models.PositiveIntegerField(default=86400,
                                                     verbose_name=_('catalog cache time (sec)'),
                                                     help_text='default 1 day')

    top_products_cache_time = models.PositiveIntegerField(default=86400,
                                                          verbose_name=_('top products cache time (sec)'),
                                                          help_text='default 1 day')

    detail_products_cache_time = models.PositiveIntegerField(default=86400,
                                                             verbose_name=_('detail products cache time (sec)'),
                                                             help_text='default 1 day')
