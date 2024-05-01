from django.test import TestCase

from ..models import Product


class ProductModelTest(TestCase):
    """Тесты для модели класса Product."""

    @classmethod
    def setUpTestData(cls):
        """Метод создает тестовый товар."""
        cls.product = Product.objects.create(name='Test product', description='Test description', price=100)

    def test_name_label(self):
        """Тест проверяет корректность описания поля name."""
        field_label = self.product._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'Название услуги')

    def test_description_label(self):
        """Тест проверяет корректность описания поля description."""
        field_label = self.product._meta.get_field('description').verbose_name
        self.assertEquals(field_label, 'Описание услуги')

    def test_price_label(self):
        """Тест проверяет корректность описания поля price."""
        field_label = self.product._meta.get_field('price').verbose_name
        self.assertEquals(field_label, 'Цена услуги')

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
