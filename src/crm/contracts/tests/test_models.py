from django.test import TestCase

from ..models import Contract
from ...leads.tests.test_models import LeadModelMixinTest


class ContractModelMixinTest(LeadModelMixinTest, TestCase):
    """Миксин для тестов модели класса Contract."""

    @classmethod
    def setUpTestData(cls):
        """
        Метод создает тестовые данные: товар, рекламную
        компанию, потенциального клиента и контракт.
        """
        super().setUpTestData()
        cls.contract = Contract.objects.create(name='Договор',
                                               lead=cls.lead,
                                               ads=cls.ads,
                                               product=cls.product,
                                               comment='Первый контракт',
                                               cost=12000,
                                               conclusion_day='2024-01-01',
                                               start_day='2024-01-05',
                                               end_day='2024-01-30',
                                               )

class ContractModelTest(ContractModelMixinTest,TestCase):
    """Тесты для модели класса Contract."""

    def test_verbose_name_label(self):
        """Проверка заполнения verbose_name."""
        field_verboses = {'name': 'Название контракта',
                          'lead': 'Клиент',
                          'ads': 'Рекламная кампания',
                          'product': 'Услуга по контракту',
                          'document': 'Скан контракта',
                          'comment': 'Комментарий',
                          'cost': 'Стоимость контракта',
                          'conclusion_day': 'Дата заключения контракта',
                          'start_day': 'Начало действия контракта',
                          'end_day': 'Окончание действия контракта',
                          }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                error_name = f'Поле {field} ожидало значение {expected_value}'
                self.assertEqual(
                    self.contract._meta.get_field(field).verbose_name,
                    expected_value, error_name)

    def test_first_name_max_length(self):
        """Тест проверяет макcимальную длину поля name."""
        self.assertEqual(self.contract._meta.get_field('name').max_length,
            150, "Поле 'name' ожидало значение 150")

    def test_object_name_is_full_name(self):
        """Тест проверяет, что __str__ возвращает №, ФИО и услугу по контракту."""
        test_name = f"Контракт № {self.contract.pk}, клиент:{self.lead}, услуга:{self.product}"
        self.assertEqual(str(self.contract), test_name)

    def test_get_absolute_url(self):
        """Тест проверяет, что метод get_absolute_url возвращает корректный URL."""
        self.assertEqual(self.contract.get_absolute_url(), f"/contracts/{self.contract.pk}/")
