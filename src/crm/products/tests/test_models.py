from django.test import TestCase

from ..models import Product


class ProductModelMixinTest(TestCase):
    """Миксин для тестов модели класса Product."""

    @classmethod
    def setUpTestData(cls):
        """Метод создает тестовый товар."""
        cls.product = Product.objects.create(name='Test product', description='Test description', price=100)

class ProductModelTest(ProductModelMixinTest, TestCase):
    """Тесты для модели класса Product."""

    def test_verbose_name_label(self):
        """Проверка заполнения verbose_name."""
        field_verboses = {'name': 'Название услуги',
                          'description': 'Описание услуги',
                          'price': 'Цена услуги'}
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                error_name = f'Поле {field} ожидало значение {expected_value}'
                self.assertEqual(
                    self.product._meta.get_field(field).verbose_name,
                    expected_value, error_name)

    def test_name_max_length(self):
        """Тест проверяет макcимальную длину поля name."""
        max_length = self.product._meta.get_field('name').max_length
        self.assertEquals(max_length, 150)

    def test_object_name_is_name(self):
        """Тест проверяет, что __str__ возвращает значение поля name."""
        self.assertEquals(str(self.product), self.product.name)
        object_name = self.product.name
        self.assertEquals(object_name, str(self.product))

    def test_get_absolute_url(self):
        """Тест проверяет, что метод get_absolute_url возвращает корректный URL."""
        self.assertEquals(self.product.get_absolute_url(), f"/products/{self.product.id}/")
