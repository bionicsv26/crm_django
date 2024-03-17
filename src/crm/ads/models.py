from django.db import models
from django.urls import reverse

from ..products.models import Product


class Ads(models.Model):
    """Класс модели рекламной кампании."""

    class PromotionChanel(models.IntegerChoices):
        """Класс вариантов каналов продвижения рекламы."""

        SOCIAL_NETWORK = 1, 'Социальные сети'
        WEBSITE = 2, 'Собственный сайт'
        INTERNET = 3, 'Другие каналы в интернет'
        OUTDOOR_AD = 4, 'Наружная реклама'
        MAGAZINE = 5, 'Журналы и газеты'
        TV = 6, 'Телевидение'
        RADIO = 7, 'Радио'
        OTHER = 8, 'Другие варианты'

    name = models.CharField(max_length=150, verbose_name='Название рекламной кампании')
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Услуга рекламной кампании')
    promotion_channel = models.SmallIntegerField(
        choices=PromotionChanel.choices,
        default=PromotionChanel.INTERNET,
        verbose_name='Канал продвижения рекламной кампании')
    description = models.TextField(verbose_name='Описание рекламной кампании')
    budget = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Бюджет рекламной кампании')

    class Meta:
        verbose_name = 'рекламная компания'
        verbose_name_plural = 'рекламные компании'

    def get_absolute_url(self) -> str:
        """Метод возвращает абсолютный адрес рекламной кампании."""
        return reverse("crm.ads:ads_detail", args=[str(self.pk)])

    def __str__(self) -> str:
        return str(self.name)
