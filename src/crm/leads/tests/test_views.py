from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.test import Client
from django.test import TestCase
from django.urls import reverse
from django.urls import reverse_lazy

from crm.leads.forms import LeadForm
from crm.leads.models import Lead
from crm.leads.tests.test_models import LeadModelMixinTest

User = get_user_model()


class LeadMixinViewTest(LeadModelMixinTest, TestCase):
    """Миксин для тестов классов LeadView."""

    @classmethod
    def setUpTestData(cls):
        """Метод создает тестовый продукт, пользователя и клиента."""
        super().setUpTestData()
        cls.user = User.objects.create_user('test_user', password='test_password')
        cls.client = Client()


class LeadCreateViewTest(LeadMixinViewTest, TestCase):
    """Тесты для класса LeadsCreateView."""

    def setUp(self):
        """Метод подготавливает тестовые фикстуры пользователя, разрешения, клиента."""
        self.permission = Permission.objects.filter(codename__in=('add_lead', 'view_lead'))
        self.user.user_permissions.add(*self.permission)
        self.client.login(username='test_user', password='test_password')

    def test_success_url(self):
        """
        Тест проверяет, что после успешного создания нового
        клиента происходит переход на список клиентов.
        """
        form_data = {
            'first_name': 'Андрей',
            'last_name': 'Андреев',
            'email': 'test@test.com',
            'phone': 89998887766,
            'ads': self.ads.pk,
            'comment': '1000',
        }

        leads_count = Lead.objects.count()
        response = self.client.post(reverse_lazy('crm.leads:leads_create'),
                                    data=form_data,
                                    follow=True)
        self.assertEqual(Lead.objects.count(), leads_count + 1)
        self.assertRedirects(response, reverse_lazy('crm.leads:leads_list'))

    def test_form_class(self):
        """Тест проверяет, что используется форма на основе класса LeadsForm."""
        response = self.client.get(reverse('crm.leads:leads_create'))
        form = response.context['form']
        self.assertEqual(form.__class__, LeadForm)

    def test_used_correct_template(self):
        """Тест проверяет, что используется корректный шаблон."""
        response = self.client.get(reverse('crm.leads:leads_create'))
        self.assertTemplateUsed(response, 'leads/leads-create.html')

    def test_with_permission_add_lead(self):
        """
        Тест проверяет, что с разрешением add_lead
        пользователь может создавать новых клиентов.
        """
        response = self.client.get(reverse('crm.leads:leads_create'))
        self.assertEqual(response.status_code, 200)

    def test_without_permission_add_lead(self):
        """Тест проверяет, что без разрешения add_lead пользователь получает ошибку 403."""
        self.user.user_permissions.remove(self.permission[0])
        response = self.client.get(reverse('crm.leads:leads_create'))
        self.assertEqual(response.status_code, 403)


class LeadListViewTest(LeadMixinViewTest, TestCase):
    """Тесты для класса LeadListView."""

    def setUp(self):
        """Метод подготавливает тестовые фикстуры пользователя, разрешения, клиента."""
        self.permission = Permission.objects.get(codename='view_lead')
        self.user.user_permissions.add(self.permission)
        self.client.login(username='test_user', password='test_password')

    def test_count_leads_in_list(self):
        """Тест проверяет, что список потенциальных клиентов содержит 1 элемент."""
        response = self.client.get(reverse_lazy('crm.leads:leads_list'))
        self.assertEqual(len(response.context['leads']), 1)

    def test_used_correct_template(self):
        """Тест проверяет, что используется корректный шаблон."""
        response = self.client.get(reverse('crm.leads:leads_list'))
        self.assertTemplateUsed(response, 'leads/leads-list.html')

    def test_with_permission_view_lead(self):
        """
        Тест проверяет, что с разрешением view_lead пользователь
        может видеть список потенциальных клиентов.
        """
        response = self.client.get(reverse('crm.leads:leads_list'))
        self.assertEqual(response.status_code, 200)

    def test_without_permission_view_lead(self):
        """Тест проверяет, что без разрешения view_lead пользователь получает ошибку 403."""
        self.user.user_permissions.remove(self.permission)
        response = self.client.get(reverse('crm.leads:leads_list'))
        self.assertEqual(response.status_code, 403)


class LeadDetailViewTest(LeadMixinViewTest, TestCase):
    """Тесты для класса LeadDetailView."""

    def setUp(self):
        """Метод подготавливает тестовые фикстуры пользователя, разрешения, клиента."""
        self.permission = Permission.objects.get(codename='view_lead')
        self.user.user_permissions.add(self.permission)
        self.client.login(username='test_user', password='test_password')

    def test_used_correct_template(self):
        """Тест проверяет, что используется корректный шаблон."""
        response = self.client.get(reverse('crm.leads:leads_detail',
                                           kwargs={'pk': self.lead.pk}))
        self.assertTemplateUsed(response, 'leads/leads-detail.html')

    def test_with_permission_view_lead(self):
        """
        Тест проверяет, что с разрешением view_lead пользователь
        может видеть детальное описание клиента.
        """
        response = self.client.get(reverse('crm.leads:leads_detail',
                                           kwargs={'pk': self.lead.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['lead'].first_name, self.lead.first_name)
        self.assertEqual(response.context['lead'].last_name, self.lead.last_name)
        self.assertEqual(response.context['lead'].email, self.lead.email)
        self.assertEqual(response.context['lead'].phone, self.lead.phone)
        self.assertEqual(response.context['lead'].ads.pk, self.lead.ads.pk)
        self.assertEqual(response.context['lead'].comment, self.lead.comment)
        self.assertEqual(response.context['lead'].to_active, self.lead.to_active)

    def test_without_permission_view_lead(self):
        """Тест проверяет, что без разрешения view_leads пользователь получает ошибку 403."""
        self.user.user_permissions.remove(self.permission)
        response = self.client.get(reverse('crm.leads:leads_detail',
                                           kwargs={'pk': self.lead.pk}))
        self.assertEqual(response.status_code, 403)


class LeadUpdateViewTest(LeadMixinViewTest, TestCase):
    """Тесты для класса LeadUpdateView."""

    def setUp(self):
        """Метод подготавливает тестовые фикстуры пользователя, разрешения, клиента."""
        self.permission = Permission.objects.get(codename='change_lead')
        self.user.user_permissions.add(self.permission)
        self.client.login(username='test_user', password='test_password')

    def test_success_update_lead(self):
        """
        Тест проверяет, что после успешного обновления данных
        компании пользователь направляется на список клиентов.
        """
        update_data = {
            'first_name': 'Андрей',
            'last_name': 'Андреев',
            'email': 'test2@test.com',
            'phone': 98765432100,
            'ads': self.ads.pk,
            'comment': 'Новый клиент',
            'to_active': False
        }

        response = self.client.post(reverse_lazy('crm.leads:leads_edit',
                                                 kwargs={'pk': self.lead.pk}),
                                    data=update_data)

        lead_after_update = Lead.objects.get(pk=self.lead.pk)
        self.assertEqual(lead_after_update.first_name, update_data['first_name'])
        self.assertEqual(lead_after_update.last_name, update_data['last_name'])
        self.assertEqual(lead_after_update.email, update_data['email'])
        self.assertEqual(lead_after_update.comment, update_data['comment'])
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse_lazy('crm.leads:leads_list'))

    def test_used_correct_template(self):
        """Тест проверяет, что используется корректный шаблон."""
        response = self.client.get(reverse('crm.leads:leads_edit',
                                           kwargs={'pk': self.lead.pk}))
        self.assertTemplateUsed(response, 'leads/leads-edit.html')

    def test_with_permission_change_lead(self):
        """
        Тест проверяет, что с разрешением change_lead
        пользователь может изменять данные клиента.
        """
        response = self.client.get(reverse('crm.leads:leads_edit',
                                           kwargs={'pk': self.lead.pk}))
        self.assertEqual(response.status_code, 200)

    def test_without_permission_change_lead(self):
        """Тест проверяет, что без разрешения change_lead пользователь получает ошибку 403."""
        self.user.user_permissions.remove(self.permission)
        response = self.client.get(reverse('crm.leads:leads_edit',
                                           kwargs={'pk': self.lead.pk}))
        self.assertEqual(response.status_code, 403)


class LeadDeleteViewTest(LeadMixinViewTest, TestCase):
    """Тесты для класса LeadDeleteView."""

    def setUp(self):
        """Метод подготавливает тестовые фикстуры пользователя, разрешения, клиента."""
        self.permission = Permission.objects.get(codename='delete_lead')
        self.user.user_permissions.add(self.permission)
        self.client.login(username='test_user', password='test_password')

    def test_success_delete_lead(self):
        """
        Тест проверяет, что после успешного удаления клиента
        пользователь направляется на список клиентов.
        """
        lead_count = Lead.objects.count()
        response = self.client.post(reverse_lazy('crm.leads:leads_delete',
                                                 kwargs={'pk': self.lead.pk}))
        self.assertEqual(Lead.objects.count(), lead_count - 1)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse_lazy('crm.leads:leads_list'))

    def test_used_correct_template(self):
        """Тест проверяет, что используется корректный шаблон."""
        response = self.client.get(reverse('crm.leads:leads_delete', kwargs={'pk': self.lead.pk}))
        self.assertTemplateUsed(response, 'leads/leads-delete.html')

    def test_with_permission_delete_lead(self):
        """Тест проверяет, что с разрешением delete_lead пользователь может удалять клиентов."""
        response = self.client.get(reverse('crm.leads:leads_delete', kwargs={'pk': self.lead.pk}))
        self.assertEqual(response.status_code, 200)

    def test_without_permission_delete_lead(self):
        """Тест проверяет, что без разрешения delete_lead пользователь получает ошибку 403."""
        self.user.user_permissions.remove(self.permission)
        response = self.client.get(reverse('crm.leads:leads_delete', kwargs={'pk': self.lead.pk}))
        self.assertEqual(response.status_code, 403)

class LeadTransferToActiveViewTest(LeadMixinViewTest, TestCase):
    """Тесты для класса LeadTransferToActiveView."""

    def setUp(self):
        """Метод подготавливает тестовые фикстуры пользователя, разрешения, клиента."""
        self.permission = Permission.objects.get(codename='can_transfer_to_active')
        self.user.user_permissions.add(self.permission)
        self.client.login(username='test_user', password='test_password')

    def test_product_id_cached_and_redirects(self):
        """
        Тест проверяет, что в кэш сохраняется значение lead_id и
        происходит перенаправление к созданию покупателя.
        """
        cache.clear()
        cached_lead_id = cache.get('lead_id')
        self.assertIsNone(cached_lead_id)

        response = self.client.get(reverse('crm.leads:leads_to_active',
                                           kwargs={'pk': self.lead.pk}))
        cached_lead_id = cache.get('lead_id')
        self.assertEqual(cached_lead_id, self.lead.pk)

        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, reverse('crm.customers:customer_create'))

    def test_with_permission_can_transfer_to_active(self):
        """
        Тест проверяет, что с разрешением can_transfer_to_active
        пользователь может создавать покупателя.
        """
        response = self.client.get(reverse('crm.leads:leads_to_active',
                                           kwargs={'pk': self.lead.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('crm.customers:customer_create'))

    def test_without_permission_can_transfer_to_active(self):
        """
        Тест проверяет, что без разрешения can_transfer_to_active
        пользователь получает ошибку 403.
        """
        self.user.user_permissions.remove(self.permission)
        response = self.client.get(reverse('crm.leads:leads_to_active',
                                           kwargs={'pk': self.lead.pk}))
        self.assertEqual(response.status_code, 403)


class LeadTransferToContractViewTest(LeadMixinViewTest, TestCase):
    """Тесты для класса LeadTransferToContractView."""

    def setUp(self):
        """Метод подготавливает тестовые фикстуры пользователя, разрешения, клиента."""
        self.permission = Permission.objects.get(codename='add_contract')
        self.user.user_permissions.add(self.permission)
        self.client.login(username='test_user', password='test_password')

    def test_product_id_cached_and_redirects(self):
        """
        Тест проверяет, что в кэш сохраняется значение lead_id и
        происходит перенаправление к созданию контракта.
        """
        cache.clear()
        cached_lead_id = cache.get('lead_id')
        self.assertIsNone(cached_lead_id)

        response = self.client.get(reverse('crm.leads:leads_to_contract',
                                           kwargs={'pk': self.lead.pk}))
        cached_lead_id = cache.get('lead_id')
        self.assertEqual(cached_lead_id, self.lead.pk)

        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, reverse('crm.contracts:contract_create'))

    def test_with_permission_can_transfer_to_contract(self):
        """
        Тест проверяет, что с разрешением can_transfer_to_contract
        пользователь может создавать контракт.
        """
        response = self.client.get(reverse('crm.leads:leads_to_contract',
                                           kwargs={'pk': self.lead.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('crm.contracts:contract_create'))

    def test_without_permission_can_transfer_to_contract(self):
        """
        Тест проверяет, что без разрешения can_transfer_to_contract
        пользователь получает ошибку 403.
        """
        self.user.user_permissions.remove(self.permission)
        response = self.client.get(reverse('crm.leads:leads_to_contract',
                                           kwargs={'pk': self.lead.pk}))
        self.assertEqual(response.status_code, 403)
