from django.db import models
from django.urls import reverse


class Product(models.Model):
    """Класс модели товара (услуги)."""

    name = models.CharField(max_length=150, verbose_name='Название услуги')
    description = models.TextField(verbose_name='Описание услуги')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена услуги')

    class Meta:
        verbose_name = 'услуга'
        verbose_name_plural = 'услуги'

    def get_absolute_url(self) -> str:
        """Метод возвращает абсолютный адрес данного товара (услуги)."""
        return reverse("crm.products:product_detail", args=[str(self.pk)])

    def __str__(self) -> str:
        return str(self.name)
