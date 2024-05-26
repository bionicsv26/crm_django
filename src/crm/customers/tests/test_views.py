from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import Client
from django.test import TestCase
from django.urls import reverse
from django.urls import reverse_lazy

from crm.customers.forms import CustomerForm
from crm.customers.models import Customer
from crm.customers.tests.test_models import CustomerModelMixinTest

User = get_user_model()


class CustomerMixinViewTest(CustomerModelMixinTest, TestCase):
    """Миксин для тестов классов ContractView."""

    @classmethod
    def setUpTestData(cls):
        """Метод создает тестовый продукт, пользователя и клиента."""
        super().setUpTestData()
        cls.user = User.objects.create_user('test_user', password='test_password')
        cls.client = Client()


class CustomerCreateViewTest(CustomerMixinViewTest, TestCase):
    """Тесты для класса CustomerCreateView."""

    def setUp(self):
        """Метод подготавливает тестовые фикстуры пользователя, разрешения, клиента."""
        self.permission = Permission.objects.filter(codename__in=('add_customer', 'view_customer'))
        self.user.user_permissions.add(*self.permission)
        self.client.login(username='test_user', password='test_password')

    def test_success_url(self):
        """
        Тест проверяет, что после успешного создания покупателя происходит переход на список покупателей.
        """
        form_data = {
            'lead': self.lead.pk,
            'ads': self.ads.pk,
            'contract': self.contract.pk,
            'comment': '2222',
        }

        customer_count = Customer.objects.count()
        response = self.client.post(reverse_lazy('crm.customers:customer_create'), data=form_data, follow=True)
        self.assertEqual(Customer.objects.count(), customer_count + 1)
        self.assertRedirects(response, reverse_lazy('crm.customers:customers_list'))

    def test_form_class(self):
        """Тест проверяет, что используется форма на основе класса CustomerForm."""
        response = self.client.get(reverse('crm.customers:customer_create'))
        form = response.context['form']
        self.assertEqual(form.__class__, CustomerForm)

    def test_used_correct_template(self):
        """Тест проверяет, что используется корректный шаблон."""
        response = self.client.get(reverse('crm.customers:customer_create'))
        self.assertTemplateUsed(response, 'customers/customers-create.html')

    def test_with_permission_add_customer(self):
        """Тест проверяет, что с разрешением add_customer пользователь может создавать пользователей."""
        response = self.client.get(reverse('crm.customers:customer_create'))
        self.assertEqual(response.status_code, 200)

    def test_without_permission_add_customer(self):
        """Тест проверяет, что без разрешения add_customer пользователь получает ошибку 403."""
        self.user.user_permissions.remove(self.permission[0])
        response = self.client.get(reverse('crm.customers:customer_create'))
        self.assertEqual(response.status_code, 403)


class CustomerListViewTest(CustomerMixinViewTest, TestCase):
    """Тесты для класса CustomerListView."""

    def setUp(self):
        """Метод подготавливает тестовые фикстуры пользователя, разрешения, клиента."""
        self.permission = Permission.objects.get(codename='view_customer')
        self.user.user_permissions.add(self.permission)
        self.client.login(username='test_user', password='test_password')

    def test_count_customer_in_list(self):
        """Тест проверяет, что список покупателей содержит 1 элемент."""
        response = self.client.get(reverse_lazy('crm.customers:customers_list'))
        self.assertEqual(len(response.context['customers']), 1)

    def test_used_correct_template(self):
        """Тест проверяет, что используется корректный шаблон."""
        response = self.client.get(reverse('crm.customers:customers_list'))
        self.assertTemplateUsed(response, 'customers/customers-list.html')

    def test_with_permission_view_customer(self):
        """Тест проверяет, что с разрешением view_customer пользователь может видеть список покупателей."""
        response = self.client.get(reverse('crm.customers:customers_list'))
        self.assertEqual(response.status_code, 200)

    def test_without_permission_view_customer(self):
        """Тест проверяет, что без разрешения view_customer пользователь получает ошибку 403."""
        self.user.user_permissions.remove(self.permission)
        response = self.client.get(reverse('crm.customers:customers_list'))
        self.assertEqual(response.status_code, 403)


class CustomerDetailViewTest(CustomerMixinViewTest, TestCase):
    """Тесты для класса CustomerDetailView."""

    def setUp(self):
        """Метод подготавливает тестовые фикстуры пользователя, разрешения, клиента."""
        self.permission = Permission.objects.get(codename='view_customer')
        self.user.user_permissions.add(self.permission)
        self.client.login(username='test_user', password='test_password')

    def test_used_correct_template(self):
        """Тест проверяет, что используется корректный шаблон."""
        response = self.client.get(reverse('crm.customers:customer_detail', kwargs={'pk': self.customer.pk}))
        self.assertTemplateUsed(response, 'customers/customers-detail.html')

    def test_with_permission_view_customer(self):
        """Тест проверяет, что с разрешением view_customer пользователь может видеть детальное описание покупателя."""
        response = self.client.get(reverse('crm.customers:customer_detail', kwargs={'pk': self.customer.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['customer'].lead.pk, self.customer.lead.pk)
        self.assertEqual(response.context['customer'].ads.pk, self.customer.ads.pk)
        self.assertEqual(response.context['customer'].contract.pk, self.customer.contract.pk)
        self.assertEqual(response.context['customer'].comment, self.customer.comment)

    def test_without_permission_view_customer(self):
        """Тест проверяет, что без разрешения view_contract пользователь получает ошибку 403."""
        self.user.user_permissions.remove(self.permission)
        response = self.client.get(reverse('crm.customers:customer_detail', kwargs={'pk': self.customer.pk}))
        self.assertEqual(response.status_code, 403)


class CustomerUpdateViewTest(CustomerMixinViewTest, TestCase):
    """Тесты для класса CustomerUpdateView."""

    def setUp(self):
        """Метод подготавливает тестовые фикстуры пользователя, разрешения, клиента."""
        self.permission = Permission.objects.get(codename='change_customer')
        self.user.user_permissions.add(self.permission)
        self.client.login(username='test_user', password='test_password')

    def test_success_update_contract(self):
        """
        Тест проверяет, что после успешного обновления данных покупателя пользователь направляется на список покупателей.
        """
        update_data = {
            'lead': self.lead.pk,
            'ads': self.ads.pk,
            'contract': self.contract.pk,
            'comment': '4444',
        }

        response = self.client.post(reverse_lazy('crm.customers:customer_edit', kwargs={'pk': self.customer.pk}),
                                    data=update_data)

        customer_after_update = Customer.objects.get(pk=self.customer.pk)
        self.assertEqual(customer_after_update.lead.pk, update_data['lead'])
        self.assertEqual(customer_after_update.ads.pk, update_data['ads'])
        self.assertEqual(customer_after_update.contract.pk, update_data['contract'])
        self.assertEqual(customer_after_update.comment, update_data['comment'])
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse_lazy('crm.customers:customers_list'))

    def test_used_correct_template(self):
        """Тест проверяет, что используется корректный шаблон."""
        response = self.client.get(reverse('crm.customers:customer_edit', kwargs={'pk': self.customer.pk}))
        self.assertTemplateUsed(response, 'customers/customers-edit.html')

    def test_with_permission_change_customer(self):
        """Тест проверяет, что с разрешением change_customer пользователь может изменять данные покупателя."""
        response = self.client.get(reverse('crm.customers:customer_edit', kwargs={'pk': self.customer.pk}))
        self.assertEqual(response.status_code, 200)

    def test_without_permission_change_customer(self):
        """Тест проверяет, что без разрешения change_customer пользователь получает ошибку 403."""
        self.user.user_permissions.remove(self.permission)
        response = self.client.get(reverse('crm.customers:customer_edit', kwargs={'pk': self.customer.pk}))
        self.assertEqual(response.status_code, 403)


class CustomerDeleteViewTest(CustomerMixinViewTest, TestCase):
    """Тесты для класса CustomerDeleteView."""

    def setUp(self):
        """Метод подготавливает тестовые фикстуры пользователя, разрешения, клиента."""
        self.permission = Permission.objects.get(codename='delete_customer')
        self.user.user_permissions.add(self.permission)
        self.client.login(username='test_user', password='test_password')

    def test_success_delete_contractcustomer(self):
        """Тест проверяет, что после успешного удаления покупателя пользователь направляется на список покупателей."""
        customer_count = Customer.objects.count()
        response = self.client.post(reverse_lazy('crm.customers:customer_delete', kwargs={'pk': self.customer.pk}))
        self.assertEqual(Customer.objects.count(), customer_count - 1)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse_lazy('crm.customers:customers_list'))

    def test_used_correct_template(self):
        """Тест проверяет, что используется корректный шаблон."""
        response = self.client.get(reverse('crm.customers:customer_delete', kwargs={'pk': self.customer.pk}))
        self.assertTemplateUsed(response, 'customers/customers-delete.html')

    def test_with_permission_delete_customer(self):
        """Тест проверяет, что с разрешением delete_customer пользователь может удалять покупателей."""
        response = self.client.get(reverse('crm.customers:customer_delete', kwargs={'pk': self.customer.pk}))
        self.assertEqual(response.status_code, 200)

    def test_without_permission_delete_customer(self):
        """Тест проверяет, что без разрешения delete_customer пользователь получает ошибку 403."""
        self.user.user_permissions.remove(self.permission)
        response = self.client.get(reverse('crm.customers:customer_delete', kwargs={'pk': self.customer.pk}))
        self.assertEqual(response.status_code, 403)
