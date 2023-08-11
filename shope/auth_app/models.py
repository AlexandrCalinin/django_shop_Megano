from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    username = models.CharField(unique=True, default="", max_length=48, null=False, blank=False)
    email = models.EmailField(unique=True, default="", null=False, blank=False)
    middle_name = models.CharField(default="", null=False, blank=False, max_length=48)
    activation_key = models.CharField(default="", null=False, blank=False, max_length=48)
    activation_key_expires = models.CharField(default="", null=False, blank=False, max_length=48)
    is_activation_key_expires = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
