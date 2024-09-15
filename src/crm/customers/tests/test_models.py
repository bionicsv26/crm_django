from django.test import TestCase

from ..models import Customer
from ...contracts.tests.test_models import ContractModelMixinTest


class CustomerModelMixinTest(ContractModelMixinTest, TestCase):
    """Миксин для тестов модели класса Customer."""

    @classmethod
    def setUpTestData(cls):
        """
        Метод создает тестовые данные: товар, рекламную компанию,
        потенциального клиента, контракт и покупателя.
        """
        super().setUpTestData()
        cls.lead.to_active = True
        cls.customer = Customer.objects.create(lead=cls.lead,
                                               ads=cls.ads,
                                               contract=cls.contract,
                                               comment='Первый комментарий по покупателю',
                                               )

class CustomerModelTest(CustomerModelMixinTest,TestCase):
    """Тесты для модели класса Customer."""

    def test_verbose_name_label(self):
        """Проверка заполнения verbose_name."""
        field_verboses = {'lead': 'Покупатель',
                          'ads': 'Рекламная кампания',
                          'contract': 'Контракт',
                          'comment': 'Комментарий',
                          }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                error_name = f'Поле {field} ожидало значение {expected_value}'
                self.assertEqual(
                    self.customer._meta.get_field(field).verbose_name,
                    expected_value, error_name)

    def test_object_name_is_full_name(self):
        """Тест проверяет, что __str__ возвращает имя и фамилию покупателя."""
        test_name = f"Клиент:{self.lead.first_name} {self.lead.last_name}"
        self.assertEqual(str(self.customer), test_name)

    def test_get_absolute_url(self):
        """Тест проверяет, что метод get_absolute_url возвращает корректный URL."""
        self.assertEqual(self.customer.get_absolute_url(), f"/customers/{self.customer.pk}/")
