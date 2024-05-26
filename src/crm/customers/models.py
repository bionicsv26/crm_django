from django.db import models
from django.urls import reverse

from ..ads.models import Ads
from ..contracts.models import Contract
from ..leads.models import Lead


class Customer(models.Model):
    """Класс модели покупателя."""

    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, verbose_name='Покупатель')
    ads = models.ForeignKey(Ads, on_delete=models.CASCADE, verbose_name='Рекламная кампания')
    contract = models.ForeignKey(Contract,
                                 on_delete=models.CASCADE,
                                 blank=True,
                                 null=True,
                                 verbose_name='Контракт'
                                 )
    comment = models.TextField(blank=True, verbose_name='Комментарий')

    class Meta:
        verbose_name = 'покупатель'
        verbose_name_plural = 'покупатели'

    def get_absolute_url(self) -> str:
        """Метод возвращает абсолютный адрес контракта."""
        return reverse("crm.customers:customer_detail", args=[str(self.pk)])

    def __str__(self) -> str:
        return f"Клиент:{self.lead.first_name} {self.lead.last_name}"
