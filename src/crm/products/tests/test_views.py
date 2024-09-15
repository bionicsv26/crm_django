from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.test import Client
from django.test import TestCase
from django.urls import reverse
from django.urls import reverse_lazy

from crm.products.forms import ProductForm
from crm.products.models import Product
from crm.products.tests.test_models import ProductModelMixinTest

User = get_user_model()


class ProductMixinViewTest(ProductModelMixinTest, TestCase):
    """Миксин для тестов классов ProductView."""

    @classmethod
    def setUpTestData(cls):
        """Метод создает тестовый продукт, пользователя и клиента."""
        super().setUpTestData()
        cls.user = User.objects.create_user('test_user', password='test_password')
        cls.client = Client()


class ProductCreateViewTest(ProductMixinViewTest, TestCase):
    """Тесты для класса ProductCreateView."""

    def setUp(self):
        """Метод подготавливает тестовые фикстуры пользователя, разрешения, клиента."""
        self.permission = Permission.objects.filter(codename__in=('add_product', 'view_product'))
        self.user.user_permissions.add(*self.permission)
        self.client.login(username='test_user', password='test_password')

    def test_success_url(self):
        """
        Тест проверяет, что после успешного создания нового
        товара (услуги) происходит переход на список товаров.
        """
        form_data = {
            'name': 'Test new product',
            'description': 'Test description of new product',
            'price': 100,
        }

        products_count = Product.objects.count()
        response = self.client.post(reverse_lazy('crm.products:product_create'),
                                    data=form_data,
                                    follow=True)
        self.assertEqual(Product.objects.count(), products_count + 1)
        self.assertRedirects(response, reverse_lazy('crm.products:products_list'))

    def test_form_class(self):
        """Тест проверяет, что используется форма на основе класса ProductForm."""
        response = self.client.get(reverse('crm.products:product_create'))
        view = response.context_data['view']
        self.assertEqual(view.form_class, ProductForm)

    def test_used_correct_template(self):
        """Тест проверяет, что используется корректный шаблон."""
        response = self.client.get(reverse('crm.products:product_create'))
        self.assertTemplateUsed(response, 'products/products-create.html')

    def test_with_permission_add_product(self):
        """
        Тест проверяет, что с разрешением add_product
        пользователь может создавать новые товары.
        """
        response = self.client.get(reverse('crm.products:product_create'))
        self.assertEqual(response.status_code, 200)

    def test_without_permission_add_product(self):
        """Тест проверяет, что без разрешения add_product пользователь получает ошибку 403."""
        self.user.user_permissions.remove(self.permission[0])
        response = self.client.get(reverse('crm.products:product_create'))
        self.assertEqual(response.status_code, 403)


class ProductListViewTest(ProductMixinViewTest, TestCase):
    """Тесты для класса ProductListView."""

    def setUp(self):
        """Метод подготавливает тестовые фикстуры пользователя, разрешения, клиента."""
        self.permission = Permission.objects.get(codename='view_product')
        self.user.user_permissions.add(self.permission)
        self.client.login(username='test_user', password='test_password')

    def test_count_products_in_list(self):
        """Тест проверяет, что список товаров (услуг) содержит 1 элемент."""
        response = self.client.get(reverse_lazy('crm.products:products_list'))
        self.assertEqual(len(response.context['products']), 1)

    def test_used_correct_template(self):
        """Тест проверяет, что используется корректный шаблон."""
        response = self.client.get(reverse('crm.products:products_list'))
        self.assertTemplateUsed(response, 'products/products-list.html')

    def test_with_permission_view_product(self):
        """
        Тест проверяет, что с разрешением view_product
        пользователь может видеть список товаров.
        """
        response = self.client.get(reverse('crm.products:products_list'))
        self.assertEqual(response.status_code, 200)

    def test_without_permission_view_product(self):
        """Тест проверяет, что без разрешения view_product пользователь получает ошибку 403."""
        self.user.user_permissions.remove(self.permission)
        response = self.client.get(reverse('crm.products:products_list'))
        self.assertEqual(response.status_code, 403)


class ProductDetailViewTest(ProductMixinViewTest, TestCase):
    """Тесты для класса ProductDetailView."""

    def setUp(self):
        """Метод подготавливает тестовые фикстуры пользователя, разрешения, клиента."""
        self.permission = Permission.objects.get(codename='view_product')
        self.user.user_permissions.add(self.permission)
        self.client.login(username='test_user', password='test_password')

    def test_used_correct_template(self):
        """Тест проверяет, что используется корректный шаблон."""
        response = self.client.get(reverse('crm.products:product_detail',
                                           kwargs={'pk': self.product.pk}))
        self.assertTemplateUsed(response, 'products/products-detail.html')

    def test_with_permission_view_product(self):
        """
        Тест проверяет, что с разрешением view_product
        пользователь может видеть детальное описание товара.
        """
        response = self.client.get(reverse('crm.products:product_detail',
                                           kwargs={'pk': self.product.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['product'].name, 'Test product')

    def test_without_permission_view_product(self):
        """Тест проверяет, что без разрешения view_product пользователь получает ошибку 403."""
        self.user.user_permissions.remove(self.permission)
        response = self.client.get(reverse('crm.products:product_detail',
                                           kwargs={'pk': self.product.pk}))
        self.assertEqual(response.status_code, 403)


class ProductUpdateViewTest(ProductMixinViewTest, TestCase):
    """Тесты для класса ProductUpdateView."""

    def setUp(self):
        """Метод подготавливает тестовые фикстуры пользователя, разрешения, клиента."""
        self.permission = Permission.objects.get(codename='change_product')
        self.user.user_permissions.add(self.permission)
        self.client.login(username='test_user', password='test_password')

    def test_success_update_product(self):
        """
        Тест проверяет, что после успешного обновления данных
        товара пользователь направляется на страницу товара.
        """
        update_data = {
            'name': 'Test New Product',
            'description': 'Test new description',
            'price': 222,
        }

        response = self.client.post(reverse_lazy('crm.products:product_edit',
                                                 kwargs={'pk': self.product.pk}),
                                    data=update_data)
        product_after_update = Product.objects.get(pk=self.product.pk)
        self.assertEqual(product_after_update.name, update_data['name'])
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse_lazy('crm.products:product_detail',
                                                    kwargs={'pk': self.product.pk}))

    def test_used_correct_template(self):
        """Тест проверяет, что используется корректный шаблон."""
        response = self.client.get(reverse('crm.products:product_edit',
                                           kwargs={'pk': self.product.pk}))
        self.assertTemplateUsed(response, 'products/products-edit.html')

    def test_with_permission_change_product(self):
        """Тест проверяет, что с разрешением change_product пользователь может создавать новые товары."""
        response = self.client.get(reverse('crm.products:product_edit',
                                           kwargs={'pk': self.product.pk}))
        self.assertEqual(response.status_code, 200)

    def test_without_permission_change_product(self):
        """Тест проверяет, что без разрешения change_product пользователь получает ошибку 403."""
        self.user.user_permissions.remove(self.permission)
        response = self.client.get(reverse('crm.products:product_edit',
                                           kwargs={'pk': self.product.pk}))
        self.assertEqual(response.status_code, 403)


class ProductDeleteViewTest(ProductMixinViewTest, TestCase):
    """Тесты для класса ProductDeleteView."""

    def setUp(self):
        """Метод подготавливает тестовые фикстуры пользователя, разрешения, клиента."""
        self.permission = Permission.objects.get(codename='delete_product')
        self.user.user_permissions.add(self.permission)
        self.client.login(username='test_user', password='test_password')

    def test_success_delete_product(self):
        """
        Тест проверяет, что после успешного удаления товара
        пользователь направляется на список товаров.
        """
        products_count = Product.objects.count()
        response = self.client.post(reverse_lazy('crm.products:product_delete',
                                                 kwargs={'pk': self.product.pk}))
        self.assertEqual(Product.objects.count(), products_count - 1)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse_lazy('crm.products:products_list'))

    def test_used_correct_template(self):
        """Тест проверяет, что используется корректный шаблон."""
        response = self.client.get(reverse('crm.products:product_delete',
                                           kwargs={'pk': self.product.pk}))
        self.assertTemplateUsed(response, 'products/products-delete.html')

    def test_with_permission_delete_product(self):
        """Тест проверяет, что с разрешением delete_product пользователь может удалять товары."""
        response = self.client.get(reverse('crm.products:product_delete',
                                           kwargs={'pk': self.product.pk}))
        self.assertEqual(response.status_code, 200)

    def test_without_permission_delete_product(self):
        """Тест проверяет, что без разрешения delete_product пользователь получает ошибку 403."""
        self.user.user_permissions.remove(self.permission)
        response = self.client.get(reverse('crm.products:product_delete',
                                           kwargs={'pk': self.product.pk}))
        self.assertEqual(response.status_code, 403)


class ProductTransferToAdsViewTest(ProductMixinViewTest, TestCase):
    """Тесты для класса ProductTransferToAdsView."""

    def setUp(self):
        """Метод подготавливает тестовые фикстуры пользователя, разрешения, клиента."""
        self.permission = Permission.objects.get(codename='add_ads')
        self.user.user_permissions.add(self.permission)
        self.client.login(username='test_user', password='test_password')

    def test_product_id_cached_and_redirects(self):
        """
        Тест проверяет, что в кэш сохраняется значение product_id и
        происходит перенаправление к созданию рекламной компании.
        """
        cache.clear()
        cached_product_id = cache.get('product_id')
        self.assertIsNone(cached_product_id)

        response = self.client.get(reverse('crm.products:product_to_ads',
                                           kwargs={'pk': self.product.pk}))
        cached_product_id = cache.get('product_id')
        self.assertEqual(cached_product_id, self.product.pk)

        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, reverse('crm.ads:ads_create'))

    def test_with_permission_add_ads(self):
        """
        Тест проверяет, что с разрешением add_ads
        пользователь может создавать рекламную кампанию.
        """
        response = self.client.get(reverse('crm.products:product_to_ads',
                                           kwargs={'pk': self.product.pk}))
        self.assertEqual(response.status_code, 302)

    def test_without_permission_add_ads(self):
        """Тест проверяет, что без разрешения add_ads пользователь получает ошибку 403."""
        self.user.user_permissions.remove(self.permission)
        response = self.client.get(reverse('crm.products:product_to_ads',
                                           kwargs={'pk': self.product.pk}))
        self.assertEqual(response.status_code, 403)
