from django.db import models
from django.urls import reverse

from .service import UnicodeNameValidator, UnicodeNumberValidator
from ..ads.models import Ads


class Lead(models.Model):
    """Класс модели потенциального клиента."""

    name_validator = UnicodeNameValidator()
    number_validator = UnicodeNumberValidator()

    first_name = models.CharField(max_length=150,
                                  validators=[name_validator],
                                  verbose_name='Имя потенциального клиента')
    last_name = models.CharField(max_length=150,
                                 validators=[name_validator],
                                 verbose_name='Фамилия потенциального клиента')
    email = models.EmailField(blank=True, verbose_name='Почта потенциального клиента')
    phone = models.CharField(max_length=14,
                             validators=[number_validator],
                             verbose_name='Телефон потенциального клиента')
    ads = models.ForeignKey(
        Ads,
        on_delete=models.CASCADE,
        verbose_name='Рекламная кампания')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    to_active = models.BooleanField(default=False, verbose_name='Перевод в активные')

    class Meta:
        verbose_name = 'потенциальный клиент'
        verbose_name_plural = 'потенциальные клиенты'
        permissions = [("can_transfer_to_active", "Can transfer to active")]

    def get_absolute_url(self) -> str:
        """Метод возвращает абсолютный адрес потенциального клиента."""
        return reverse("crm.leads:leads_detail", args=[str(self.pk)])

    def __str__(self) -> str:
        full_name: str = f"{self.first_name} {self.last_name}"
        return full_name.strip()

    def is_active(self) -> bool:
        """Метод проверяет переведен ли потенциальный клиент в активные."""
        return self.to_active
