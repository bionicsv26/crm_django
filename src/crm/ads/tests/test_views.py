from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.test import Client
from django.test import TestCase
from django.urls import reverse
from django.urls import reverse_lazy

from crm.ads.forms import AdsForm
from crm.ads.models import Ads
from crm.products.models import Product

User = get_user_model()


class ProductTestMixin(TestCase):
    """Тесты для класса AdsCreateView."""

    @classmethod
    def setUpTestData(cls):
        """Метод создает тестовый продукт, пользователя и клиента."""
        cls.product = Product.objects.create(name="Test Product",
                                             description="Test description",
                                             price=10.0,
                                             )
        cls.user = User.objects.create_user('test_user', password='test_password')
        cls.client = Client()

    def setUp(self):
        """Метод подготавливает тестовые фикстуры пользователя, разрешения, клиента."""
        # self.permission = Permission.objects.filter(codename__in=('add_ads', 'view_ads'))
        # self.user.user_permissions.add(*self.permission)
        self.client.login(username='test_user', password='test_password')


class AdsCreateViewTest(ProductTestMixin, TestCase):
    """Тесты для класса AdsCreateView."""

    # @classmethod
    # def setUpTestData(cls):
    #     """Метод создает тестовый продукт, пользователя и клиента."""
    #     cls.product = Product.objects.create(name="Test Product",
    #                                          description="Test description",
    #                                          price=10.0,
    #                                          )
    #     cls.user = User.objects.create_user('test_user', password='test_password')
    #     cls.client = Client()

    def setUp(self):
        """Метод подготавливает тестовые фикстуры пользователя, разрешения, клиента."""
        self.permission = Permission.objects.filter(codename__in=('add_ads', 'view_ads'))
        self.user.user_permissions.add(*self.permission)
        super().setUp()

    def test_success_url(self):
        """
        Тест проверяет, что после успешного создания новой рекламной компании происходит переход на список компаний.
        """
        form_data = {
            'name': 'Test ads',
            'description': 'Test ads description',
            'promotion_channel': Ads.PromotionChanel.INTERNET,
            'budget': 1000,
            'product': self.product.pk,
        }

        ads_count = Ads.objects.count()
        response = self.client.post(reverse_lazy('crm.ads:ads_create'), data=form_data, follow=True)
        self.assertEqual(Ads.objects.count(), ads_count + 1)
        self.assertRedirects(response, reverse_lazy('crm.ads:ads_list'))

    def test_form_class(self):
        """Тест проверяет, что используется форма на основе класса AdsForm."""
        response = self.client.get(reverse('crm.ads:ads_create'))
        form = response.context['form']
        self.assertEqual(form.__class__, AdsForm)

    def test_used_correct_template(self):
        """Тест проверяет, что используется корректный шаблон."""
        response = self.client.get(reverse('crm.ads:ads_create'))
        self.assertTemplateUsed(response, 'ads/ads-create.html')

    def test_with_permission_add_product(self):
        """Тест проверяет, что с разрешением add_ads пользователь может создавать новые рекламные компании."""
        response = self.client.get(reverse('crm.ads:ads_create'))
        self.assertEqual(response.status_code, 200)

    def test_without_permission_add_ads(self):
        """Тест проверяет, что без разрешения add_ads пользователь получает ошибку 403."""
        self.user.user_permissions.remove(self.permission[0])
        response = self.client.get(reverse('crm.ads:ads_create'))
        self.assertEqual(response.status_code, 403)


class AdsListViewTest(TestCase):
    """Тесты для класса AdsListView."""

    @classmethod
    def setUpTestData(cls):
        """Метод подготавливает тестовые фикстуры списка , создает пользователя и клиента."""
        for idx in range(1, 4):
            cls.product = Product.objects.create(name=f"Test Product {idx}",
                                                 description=f"Test description {idx}",
                                                 price=10.0 * idx,
                                                 )
            Ads.objects.create(name=f"Test ads {idx}",
                               description=f"Test ads description {idx}",
                               budget=1000 * idx,
                               product=cls.product
                               )
        cls.user = User.objects.create_user('test_user', password='test_password')
        cls.client = Client()

    def setUp(self):
        """Метод подготавливает тестовые фикстуры пользователя, разрешения, клиента."""
        self.permission = Permission.objects.get(codename='view_ads')
        self.user.user_permissions.add(self.permission)
        self.client.login(username='test_user', password='test_password')

    def test_count_ads_in_list(self):
        """Тест проверяет, что список рекламных компаний содержит 3 элемента."""
        response = self.client.get(reverse_lazy('crm.ads:ads_list'))
        self.assertEqual(len(response.context['ads']), 3)

    def test_used_correct_template(self):
        """Тест проверяет, что используется корректный шаблон."""
        response = self.client.get(reverse('crm.ads:ads_list'))
        self.assertTemplateUsed(response, 'ads/ads-list.html')

    def test_with_permission_view_ads(self):
        """Тест проверяет, что с разрешением view_ads пользователь может видеть список товаров."""
        response = self.client.get(reverse('crm.ads:ads_list'))
        self.assertEqual(response.status_code, 200)

    def test_without_permission_view_ads(self):
        """Тест проверяет, что без разрешения view_ads пользователь получает ошибку 403."""
        self.user.user_permissions.remove(self.permission)
        response = self.client.get(reverse('crm.ads:ads_list'))
        self.assertEqual(response.status_code, 403)


class AdsDetailViewTest(TestCase):
    """Тесты для класса AdsDetailView."""

    @classmethod
    def setUpTestData(cls):
        """
        Метод подготавливает тестовую фикстуру товара (услуги) и рекламной компании, создает пользователя и клиента.
         """
        cls.product = Product.objects.create(name="Test Product",
                                             description="Test description",
                                             price=10.0,
                                             )
        cls.ads = Ads.objects.create(name="Test ads",
                                     description="Test ads description",
                                     budget=1000,
                                     product=cls.product
                                     )
        cls.user = User.objects.create_user('test_user', password='test_password')
        cls.client = Client()

    def setUp(self):
        """Метод подготавливает тестовые фикстуры пользователя, разрешения, клиента."""
        self.permission = Permission.objects.get(codename='view_ads')
        self.user.user_permissions.add(self.permission)
        self.client.login(username='test_user', password='test_password')

    def test_used_correct_template(self):
        """Тест проверяет, что используется корректный шаблон."""
        response = self.client.get(reverse('crm.ads:ads_detail', kwargs={'pk': self.ads.pk}))
        self.assertTemplateUsed(response, 'ads/ads-detail.html')

    def test_with_permission_view_ads(self):
        """Тест проверяет, что с разрешением view_ads пользователь может видеть детальное описание компании."""
        response = self.client.get(reverse('crm.ads:ads_detail', kwargs={'pk': self.ads.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['ads'].name, self.ads.name)
        self.assertEqual(response.context['ads'].description, self.ads.description)
        self.assertEqual(response.context['ads'].budget, self.ads.budget)
        self.assertEqual(response.context['ads'].product, self.ads.product)
        self.assertEqual(response.context['ads'].promotion_channel, self.ads.promotion_channel)

    def test_without_permission_view_ads(self):
        """Тест проверяет, что без разрешения view_ads пользователь получает ошибку 403."""
        self.user.user_permissions.remove(self.permission)
        response = self.client.get(reverse('crm.ads:ads_detail', kwargs={'pk': self.ads.pk}))
        self.assertEqual(response.status_code, 403)


class AdsUpdateViewTest(TestCase):
    """Тесты для класса AdsUpdateView."""

    @classmethod
    def setUpTestData(cls):
        """
        Метод подготавливает тестовую фикстуру товара (услуги) и рекламной компании, создает пользователя и клиента.
         """
        cls.product = Product.objects.create(name="Test Product",
                                             description="Test description",
                                             price=10.0,
                                             )
        cls.ads = Ads.objects.create(name="Test ads",
                                     description="Test ads description",
                                     budget=1000,
                                     product=cls.product
                                     )
        cls.user = User.objects.create_user('test_user', password='test_password')
        cls.client = Client()

    def setUp(self):
        """Метод подготавливает тестовые фикстуры пользователя, разрешения, клиента."""
        self.permission = Permission.objects.get(codename='change_ads')
        self.user.user_permissions.add(self.permission)
        self.client.login(username='test_user', password='test_password')

    def test_success_update_ads(self):
        """
        Тест проверяет, что после успешного обновления данных компании пользователь направляется на список компаний.
        """
        update_data = {
            'name': 'Test updated ads',
            'description': 'Test updated ads description',
            'promotion_channel': Ads.PromotionChanel.SOCIAL_NETWORK,
            'product': self.product.pk,
            'budget': 333,
        }

        response = self.client.post(reverse_lazy('crm.ads:ads_edit', kwargs={'pk': self.ads.pk}),
                                    data=update_data)

        ads_after_update = Ads.objects.get(pk=self.ads.pk)
        self.assertEqual(ads_after_update.name, update_data['name'])
        self.assertEqual(ads_after_update.description, update_data['description'])
        self.assertEqual(ads_after_update.budget, update_data['budget'])
        self.assertEqual(ads_after_update.promotion_channel, update_data['promotion_channel'])
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse_lazy('crm.ads:ads_list'))

    def test_used_correct_template(self):
        """Тест проверяет, что используется корректный шаблон."""
        response = self.client.get(reverse('crm.ads:ads_edit', kwargs={'pk': self.ads.pk}))
        self.assertTemplateUsed(response, 'ads/ads-edit.html')

    def test_with_permission_change_ads(self):
        """Тест проверяет, что с разрешением change_ads пользователь может создавать новые компании."""
        response = self.client.get(reverse('crm.ads:ads_edit', kwargs={'pk': self.ads.pk}))
        self.assertEqual(response.status_code, 200)

    def test_without_permission_change_ads(self):
        """Тест проверяет, что без разрешения change_ads пользователь получает ошибку 403."""
        self.user.user_permissions.remove(self.permission)
        response = self.client.get(reverse('crm.ads:ads_edit', kwargs={'pk': self.ads.pk}))
        self.assertEqual(response.status_code, 403)


class AdsDeleteViewTest(TestCase):
    """Тесты для класса AdsDeleteView."""

    @classmethod
    def setUpTestData(cls):
        """
        Метод подготавливает тестовую фикстуру товара (услуги) и рекламной компании, создает пользователя и клиента.
         """
        cls.product = Product.objects.create(name="Test Product",
                                             description="Test description",
                                             price=10.0,
                                             )
        cls.ads = Ads.objects.create(name="Test ads",
                                     description="Test ads description",
                                     budget=1000,
                                     product=cls.product
                                     )
        cls.user = User.objects.create_user('test_user', password='test_password')
        cls.client = Client()

    def setUp(self):
        """Метод подготавливает тестовые фикстуры пользователя, разрешения, клиента."""
        self.permission = Permission.objects.get(codename='delete_ads')
        self.user.user_permissions.add(self.permission)
        self.client.login(username='test_user', password='test_password')

    def test_success_delete_ads(self):
        """Тест проверяет, что после успешного удаления компании пользователь направляется на список компаний."""
        ads_count = Ads.objects.count()
        response = self.client.post(reverse_lazy('crm.ads:ads_delete', kwargs={'pk': self.ads.pk}))
        self.assertEqual(Ads.objects.count(), ads_count - 1)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse_lazy('crm.ads:ads_list'))

    def test_used_correct_template(self):
        """Тест проверяет, что используется корректный шаблон."""
        response = self.client.get(reverse('crm.ads:ads_delete', kwargs={'pk': self.ads.pk}))
        self.assertTemplateUsed(response, 'ads/ads-delete.html')

    def test_with_permission_delete_ads(self):
        """Тест проверяет, что с разрешением delete_ads пользователь может удалять компании."""
        response = self.client.get(reverse('crm.ads:ads_delete', kwargs={'pk': self.ads.pk}))
        self.assertEqual(response.status_code, 200)

    def test_without_permission_delete_ads(self):
        """Тест проверяет, что без разрешения delete_ads пользователь получает ошибку 403."""
        self.user.user_permissions.remove(self.permission)
        response = self.client.get(reverse('crm.ads:ads_delete', kwargs={'pk': self.ads.pk}))
        self.assertEqual(response.status_code, 403)
