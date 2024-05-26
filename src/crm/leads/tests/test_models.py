from django.test import TestCase

from ..models import Lead
from ...ads.tests.test_models import AdsModelMixinTest


class LeadModelMixinTest(AdsModelMixinTest, TestCase):
    """Миксин для тестов модели класса Lead."""

    @classmethod
    def setUpTestData(cls):
        """Метод создает тестовые данные: товар, рекламную компанию и потенциального клиента."""
        super().setUpTestData()
        cls.lead = Lead.objects.create(first_name='Иван',
                                     last_name='Иванов',
                                     email='test@test.com',
                                     phone='89996660000',
                                     ads=cls.ads,
                                     comment='Ох')

class LeadModelTest(LeadModelMixinTest,TestCase):
    """Тесты для модели класса Lead."""

    def test_verbose_name_label(self):
        """Проверка заполнения verbose_name."""
        field_verboses = {'first_name': 'Имя потенциального клиента',
                          'last_name': 'Фамилия потенциального клиента',
                          'email': 'Почта потенциального клиента',
                          'phone': 'Телефон потенциального клиента',
                          'ads': 'Рекламная кампания',
                          'comment': 'Комментарий',
                          'to_active': 'Перевод в активные'}
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                error_name = f'Поле {field} ожидало значение {expected_value}'
                self.assertEqual(
                    self.lead._meta.get_field(field).verbose_name,
                    expected_value, error_name)

    def test_to_active_value_default(self):
        """Тест проверяет значение поля to_active по умолчанию."""
        field_value = self.lead.to_active
        self.assertFalse(field_value)

    def test_first_name_max_length(self):
        """Тест проверяет макcимальную длину поля first_name."""
        field_max_lengths = {'first_name': 150,
                             'last_name': 150,
                             'phone': 14}
        for field, expected_value in field_max_lengths.items():
            with self.subTest(field=field):
                error_name = f'Поле {field} ожидало значение {expected_value}'
                self.assertEqual(
                    self.lead._meta.get_field(field).max_length,
                    expected_value, error_name)

    def test_object_name_is_full_name(self):
        """Тест проверяет, что __str__ возвращает имя и фамилию клиента."""
        self.assertEquals(str(self.lead), 'Иван Иванов')

    def test_get_absolute_url(self):
        """Тест проверяет, что метод get_absolute_url возвращает корректный URL."""
        self.assertEquals(self.lead.get_absolute_url(), f"/leads/{self.lead.id}/")
