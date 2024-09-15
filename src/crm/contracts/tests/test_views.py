import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import Client
from django.test import TestCase
from django.urls import reverse
from django.urls import reverse_lazy

from crm.contracts.forms import ContractForm
from crm.contracts.models import Contract
from crm.contracts.tests.test_models import ContractModelMixinTest

User = get_user_model()


class ContractMixinViewTest(ContractModelMixinTest, TestCase):
    """Миксин для тестов классов ContractView."""

    @classmethod
    def setUpTestData(cls):
        """Метод создает тестовый продукт, пользователя и клиента."""
        super().setUpTestData()
        cls.user = User.objects.create_user('test_user', password='test_password')
        cls.client = Client()


class ContractCreateViewTest(ContractMixinViewTest, TestCase):
    """Тесты для класса ContractCreateView."""

    def setUp(self):
        """Метод подготавливает тестовые фикстуры пользователя, разрешения, клиента."""
        self.permission = Permission.objects.filter(codename__in=('add_contract', 'view_contract'))
        self.user.user_permissions.add(*self.permission)
        self.client.login(username='test_user', password='test_password')

    def test_success_url(self):
        """
        Тест проверяет, что после успешного создания нового
        контракта происходит переход на список контрактов.
        """
        form_data = {
            'name': 'Контракт',
            'lead': self.lead.pk,
            'ads': self.ads.pk,
            'product': self.product.pk,
            'comment': '2222',
            'cost': 13500,
            'conclusion_day': '2024-02-01',
            'start_day': '2024-02-05',
            'end_day': '2024-02-28'
        }

        contract_count = Contract.objects.count()
        response = self.client.post(reverse_lazy('crm.contracts:contract_create'),
                                    data=form_data,
                                    follow=True)
        self.assertEqual(Contract.objects.count(), contract_count + 1)
        self.assertRedirects(response, reverse_lazy('crm.contracts:contracts_list'))

    def test_form_class(self):
        """Тест проверяет, что используется форма на основе класса ContractForm."""
        response = self.client.get(reverse('crm.contracts:contract_create'))
        form = response.context['form']
        self.assertEqual(form.__class__, ContractForm)

    def test_used_correct_template(self):
        """Тест проверяет, что используется корректный шаблон."""
        response = self.client.get(reverse('crm.contracts:contract_create'))
        self.assertTemplateUsed(response, 'contracts/contracts-create.html')

    def test_with_permission_add_contract(self):
        """
        Тест проверяет, что с разрешением add_contract
        пользователь может создавать новые контракты.
        """
        response = self.client.get(reverse('crm.contracts:contract_create'))
        self.assertEqual(response.status_code, 200)

    def test_without_permission_add_contract(self):
        """Тест проверяет, что без разрешения add_contract пользователь получает ошибку 403."""
        self.user.user_permissions.remove(self.permission[0])
        response = self.client.get(reverse('crm.contracts:contract_create'))
        self.assertEqual(response.status_code, 403)


class ContractListViewTest(ContractMixinViewTest, TestCase):
    """Тесты для класса ContractListView."""

    def setUp(self):
        """Метод подготавливает тестовые фикстуры пользователя, разрешения, клиента."""
        self.permission = Permission.objects.get(codename='view_contract')
        self.user.user_permissions.add(self.permission)
        self.client.login(username='test_user', password='test_password')

    def test_count_contract_in_list(self):
        """Тест проверяет, что список контрактов содержит 1 элемент."""
        response = self.client.get(reverse_lazy('crm.contracts:contracts_list'))
        self.assertEqual(len(response.context['contracts']), 1)

    def test_used_correct_template(self):
        """Тест проверяет, что используется корректный шаблон."""
        response = self.client.get(reverse('crm.contracts:contracts_list'))
        self.assertTemplateUsed(response, 'contracts/contracts-list.html')

    def test_with_permission_view_contract(self):
        """
        Тест проверяет, что с разрешением view_contract
        пользователь может видеть список контрактов.
        """
        response = self.client.get(reverse('crm.contracts:contracts_list'))
        self.assertEqual(response.status_code, 200)

    def test_without_permission_view_contract(self):
        """Тест проверяет, что без разрешения view_contract пользователь получает ошибку 403."""
        self.user.user_permissions.remove(self.permission)
        response = self.client.get(reverse('crm.contracts:contracts_list'))
        self.assertEqual(response.status_code, 403)


class ContractDetailViewTest(ContractMixinViewTest, TestCase):
    """Тесты для класса ContractDetailView."""

    def setUp(self):
        """Метод подготавливает тестовые фикстуры пользователя, разрешения, клиента."""
        self.permission = Permission.objects.get(codename='view_contract')
        self.user.user_permissions.add(self.permission)
        self.client.login(username='test_user', password='test_password')

    def test_used_correct_template(self):
        """Тест проверяет, что используется корректный шаблон."""
        response = self.client.get(reverse('crm.contracts:contract_detail',
                                           kwargs={'pk': self.contract.pk}))
        self.assertTemplateUsed(response, 'contracts/contracts-detail.html')

    def test_with_permission_view_contract(self):
        """
        Тест проверяет, что с разрешением view_contract
        пользователь может видеть детальное описание контракта.
        """
        response = self.client.get(reverse('crm.contracts:contract_detail',
                                           kwargs={'pk': self.contract.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['contract'].name, self.contract.name)
        self.assertEqual(response.context['contract'].lead.pk, self.contract.lead.pk)
        self.assertEqual(response.context['contract'].ads.pk, self.contract.ads.pk)
        self.assertEqual(response.context['contract'].product.pk, self.contract.product.pk)
        self.assertEqual(response.context['contract'].comment, self.contract.comment)
        self.assertEqual(response.context['contract'].cost, self.contract.cost)
        self.assertEqual(response.context['contract'].conclusion_day,
                         datetime.date.fromisoformat(self.contract.conclusion_day))
        self.assertEqual(response.context['contract'].start_day,
                         datetime.date.fromisoformat(self.contract.start_day))
        self.assertEqual(response.context['contract'].end_day,
                         datetime.date.fromisoformat(self.contract.end_day))

    def test_without_permission_view_contract(self):
        """Тест проверяет, что без разрешения view_contract пользователь получает ошибку 403."""
        self.user.user_permissions.remove(self.permission)
        response = self.client.get(reverse('crm.contracts:contract_detail',
                                           kwargs={'pk': self.contract.pk}))
        self.assertEqual(response.status_code, 403)


class ContractUpdateViewTest(ContractMixinViewTest, TestCase):
    """Тесты для класса ContractUpdateView."""

    def setUp(self):
        """Метод подготавливает тестовые фикстуры пользователя, разрешения, клиента."""
        self.permission = Permission.objects.get(codename='change_contract')
        self.user.user_permissions.add(self.permission)
        self.client.login(username='test_user', password='test_password')

    def test_success_update_contract(self):
        """
        Тест проверяет, что после успешного обновления данных контракта
        пользователь направляется на список контрактов.
        """
        update_data = {
            'name': 'Новый контракт',
            'lead': self.lead.pk,
            'ads': self.ads.pk,
            'product': self.product.pk,
            'comment': '3333',
            'cost': 9999,
            'conclusion_day': '2024-03-01',
            'start_day': '2024-03-05',
            'end_day': '2024-03-28'
        }

        response = self.client.post(reverse_lazy('crm.contracts:contract_edit',
                                                 kwargs={'pk': self.contract.pk}),
                                    data=update_data)

        contract_after_update = Contract.objects.get(pk=self.contract.pk)
        self.assertEqual(contract_after_update.name, update_data['name'])
        self.assertEqual(contract_after_update.lead.pk, update_data['lead'])
        self.assertEqual(contract_after_update.ads.pk, update_data['ads'])
        self.assertEqual(contract_after_update.product.pk, update_data['product'])
        self.assertEqual(contract_after_update.comment, update_data['comment'])
        self.assertEqual(contract_after_update.cost, update_data['cost'])
        self.assertEqual(contract_after_update.conclusion_day,
                         datetime.date.fromisoformat(update_data['conclusion_day']))
        self.assertEqual(contract_after_update.start_day,
                         datetime.date.fromisoformat(update_data['start_day']))
        self.assertEqual(contract_after_update.end_day,
                         datetime.date.fromisoformat(update_data['end_day']))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse_lazy('crm.contracts:contracts_list'))

    def test_used_correct_template(self):
        """Тест проверяет, что используется корректный шаблон."""
        response = self.client.get(reverse('crm.contracts:contract_edit',
                                           kwargs={'pk': self.contract.pk}))
        self.assertTemplateUsed(response, 'contracts/contracts-edit.html')

    def test_with_permission_change_contract(self):
        """
        Тест проверяет, что с разрешением change_contract
        пользователь может изменять данные контракта.
        """
        response = self.client.get(reverse('crm.contracts:contract_edit',
                                           kwargs={'pk': self.contract.pk}))
        self.assertEqual(response.status_code, 200)

    def test_without_permission_change_contract(self):
        """Тест проверяет, что без разрешения change_contract пользователь получает ошибку 403."""
        self.user.user_permissions.remove(self.permission)
        response = self.client.get(reverse('crm.contracts:contract_edit',
                                           kwargs={'pk': self.contract.pk}))
        self.assertEqual(response.status_code, 403)


class ContractDeleteViewTest(ContractMixinViewTest, TestCase):
    """Тесты для класса ContractDeleteView."""

    def setUp(self):
        """Метод подготавливает тестовые фикстуры пользователя, разрешения, клиента."""
        self.permission = Permission.objects.get(codename='delete_contract')
        self.user.user_permissions.add(self.permission)
        self.client.login(username='test_user', password='test_password')

    def test_success_delete_contract(self):
        """
        Тест проверяет, что после успешного удаления контракта
        пользователь направляется на список контрактов.
        """
        lead_count = Contract.objects.count()
        response = self.client.post(reverse_lazy('crm.contracts:contract_delete',
                                                 kwargs={'pk': self.contract.pk}))
        self.assertEqual(Contract.objects.count(), lead_count - 1)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse_lazy('crm.contracts:contracts_list'))

    def test_used_correct_template(self):
        """Тест проверяет, что используется корректный шаблон."""
        response = self.client.get(reverse('crm.contracts:contract_delete',
                                           kwargs={'pk': self.contract.pk}))
        self.assertTemplateUsed(response, 'contracts/contracts-delete.html')

    def test_with_permission_delete_contract(self):
        """
        Тест проверяет, что с разрешением delete_contract
        пользователь может удалять контракты.
        """
        response = self.client.get(reverse('crm.contracts:contract_delete',
                                           kwargs={'pk': self.contract.pk}))
        self.assertEqual(response.status_code, 200)

    def test_without_permission_delete_contract(self):
        """Тест проверяет, что без разрешения delete_contract пользователь получает ошибку 403."""
        self.user.user_permissions.remove(self.permission)
        response = self.client.get(reverse('crm.contracts:contract_delete',
                                           kwargs={'pk': self.contract.pk}))
        self.assertEqual(response.status_code, 403)
