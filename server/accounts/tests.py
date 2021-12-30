from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User


class AccountsViewTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()

        
    def test_register_user(self):
        response = self.client.post('/accounts/register',
                                    content_type="application/json",
                                    data={
                                        'email': "test@test.com",
                                        'username': "test",
                                        'first_name': 'first test',
                                        'last_name': 'last test',
                                        'password': 'password',
                                        'phone_number': '111111111',
                                    })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'success': True})
        self.assertEqual(User.objects.count(), 2)  # admin + created user
        created_user = User.objects.get(username="test")
        self.assertEqual(created_user.email, "test@test.com")
        self.assertEqual(created_user.first_name, "first test")
        self.assertEqual(created_user.last_name, "last test")
        self.assertEqual(created_user.profile.phone_number, '111111111')
        self.assertTrue(created_user.is_authenticated)
