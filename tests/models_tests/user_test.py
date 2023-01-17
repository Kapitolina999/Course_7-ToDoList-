from django.test import TestCase

from core.models import User


class UserTest(TestCase):
    def user_create(self, username='username_test', password='password_test',
                    first_name='first_name', last_name='last_name'):
        return User.objects.create(username=username, password=password,
                                   first_name=first_name, last_name=last_name)

    def test_user_creation(self):
        user = self.user_create()
        self.assertTrue(isinstance(user, User))
        self.assertEqual(user.__str__(), f'{user.first_name} {user.last_name}')

    def test_first_name_max_length(self):
        user = self.user_create()
        max_length = user._meta.get_field('first_name').max_length
        self.assertEquals(max_length, 150)

