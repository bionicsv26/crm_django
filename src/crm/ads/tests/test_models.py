from django.test import TestCase

from ..models import Ads
from ...products.models import Product


class AdsModelTest(TestCase):
    """Тесты для модели класса Ads."""

    @classmethod
    def setUpTestData(cls):
        """Метод создает тестовый товар и тестовую рекамную компанию."""
        cls.product = Product.objects.create(name='Test product',
                                             description='Test description',
                                             price=100)
        cls.ads = Ads.objects.create(name='Test ads',
                                     description='Test ads description',
                                     budget=1000,
                                     product=cls.product)

    def test_name_label(self):
        """Тест проверяет корректность описания поля name."""
        field_label = self.ads._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'Название рекламной кампании')

    def test_product_label(self):
        """Тест проверяет корректность описания поля product."""
        field_label = self.ads._meta.get_field('product').verbose_name
        self.assertEquals(field_label, 'Услуга рекламной кампании')

    def test_promotion_channel_label(self):
        """Тест проверяет корректность описания поля promotion_channel."""
        field_label = self.ads._meta.get_field('promotion_channel').verbose_name
        self.assertEquals(field_label, 'Канал продвижения рекламной кампании')

    def test_promotion_channel_value_default(self):
        """Тест проверяет значение поля promotion_channel по умолчанию."""
        field_value = self.ads.promotion_channel
        self.assertEquals(field_value, 3)

    def test_description_label(self):
        """Тест проверяет корректность описания поля description."""
        field_label = self.ads._meta.get_field('description').verbose_name
        self.assertEquals(field_label, 'Описание рекламной кампании')

    def test_budget_label(self):
        """Тест проверяет корректность описания поля budget."""
        field_label = self.ads._meta.get_field('budget').verbose_name
        self.assertEquals(field_label, 'Бюджет рекламной кампании')

    def test_name_max_length(self):
        """Тест проверяет макcимальную длину поля name."""
        max_length = self.ads._meta.get_field('name').max_length
        self.assertEquals(max_length, 150)

    def test_object_name_is_name(self):
        """Тест проверяет, что __str__ возвращает значение поля name."""
        self.assertEquals(str(self.ads), self.ads.name)
        object_name = self.ads.name
        self.assertEquals(object_name, str(self.ads))

    def test_get_absolute_url(self):
        """Тест проверяет, что метод get_absolute_url возвращает корректный URL."""

        self.assertEquals(self.ads.get_absolute_url(), f"/ads/{self.ads.id}/")
