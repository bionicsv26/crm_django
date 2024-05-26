from django.db import models
from django.urls import reverse

from ..ads.models import Ads
from ..leads.models import Lead
from ..products.models import Product


class Contract(models.Model):
    """Класс модели контракта."""

    name = models.CharField(max_length=150, verbose_name='Название контракта')
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, verbose_name='Клиент')
    ads = models.ForeignKey(Ads, on_delete=models.CASCADE, verbose_name='Рекламная кампания')
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                verbose_name='Услуга по контракту'
                                )
    document = models.FileField(upload_to='documents/',
                                blank=True,
                                null=True,
                                verbose_name='Скан контракта'
                                )
    comment = models.TextField(blank=True, null=True, verbose_name='Комментарий')
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Стоимость контракта')
    conclusion_day = models.DateField(verbose_name='Дата заключения контракта')
    start_day = models.DateField(verbose_name='Начало действия контракта')
    end_day = models.DateField(verbose_name='Окончание действия контракта')
    class Meta:
        verbose_name = 'контракт'
        verbose_name_plural = 'контракты'

    def get_absolute_url(self) -> str:
        """Метод возвращает абсолютный адрес контракта."""
        return reverse("crm.contracts:contract_detail", args=[str(self.pk)])

    def __str__(self) -> str:
        return f"Контракт № {self.pk}, клиент:{self.lead}, услуга:{self.product}"
