from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Класс для изменения стандартного пользователя джанго."""

    full_name = models.CharField(max_length=255, unique=True, verbose_name='ФИО')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'full_name'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        abstract = False
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return str(self.full_name)
