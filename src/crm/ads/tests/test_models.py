from django.test import TestCase

from ..models import Ads
from ...products.tests.test_models import ProductModelMixinTest


class AdsModelMixinTest(ProductModelMixinTest, TestCase):
    """Миксин для тестов модели класса Ads."""

    @classmethod
    def setUpTestData(cls):
        """Метод создает тестовый товар и тестовую рекламную компанию."""
        super().setUpTestData()
        cls.ads = Ads.objects.create(name='Test ads',
                                     description='Test ads description',
                                     budget=1000,
                                     product=cls.product)
class AdsModelTest(AdsModelMixinTest,TestCase):
    """Тесты для модели класса Ads."""

    def test_verbose_name_label(self):
        """Проверка заполнения verbose_name."""
        field_verboses = {'name': 'Название рекламной кампании',
                          'product': 'Услуга рекламной кампании',
                          'promotion_channel': 'Канал продвижения рекламной кампании',
                          'description': 'Описание рекламной кампании',
                          'budget': 'Бюджет рекламной кампании'}
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                error_name = f'Поле {field} ожидало значение {expected_value}'
                self.assertEqual(
                    self.ads._meta.get_field(field).verbose_name,
                    expected_value, error_name)

    def test_promotion_channel_value_default(self):
        """Тест проверяет значение поля promotion_channel по умолчанию."""
        field_value = self.ads.promotion_channel
        self.assertEqual(field_value, 3)

    def test_name_max_length(self):
        """Тест проверяет макcимальную длину поля name."""
        max_length = self.ads._meta.get_field('name').max_length
        self.assertEqual(max_length, 150)

    def test_object_name_is_name(self):
        """Тест проверяет, что __str__ возвращает значение поля name."""
        self.assertEqual(str(self.ads), self.ads.name)

    def test_get_absolute_url(self):
        """Тест проверяет, что метод get_absolute_url возвращает корректный URL."""
        self.assertEqual(self.ads.get_absolute_url(), f"/ads/{self.ads.id}/")
