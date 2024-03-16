from django.contrib.auth import get_user_model
from django.test import TestCase


class UsersManagersTests(TestCase):
    """
    Тесты класса CustomUser.
    """

    def test_create_user(self):
        """
        Тест создания обычного пользователя.
        """
        User = get_user_model()
        user = User.objects.create_user(
            full_name='Иванов Иван Иванович',
            password='123456'
        )
        self.assertEqual(user.full_name, 'Иванов Иван Иванович')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(full_name='')
        with self.assertRaises(ValueError):
            User.objects.create_user(full_name='', password="foo")

    def test_create_superuser(self):
        """
        Тест создания суперпользователя.
        """
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            full_name='Петров Иван Иванович',
            password='123456'
        )
        self.assertEqual(admin_user.full_name, 'Петров Иван Иванович')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                full_name='Петров Иван Иванович',
                password='123321',
                is_superuser=False
            )
