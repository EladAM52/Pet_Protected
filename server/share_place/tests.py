from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from .models import *
from django.urls import reverse,resolve
from .views import *
import json


class SharePlaceViewTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.create_user(username="test", first_name='test', last_name='tester',
                                             email='test@test.com', password='password')
        self.user.profile.phone_number = '123'
        self.user.save()
    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.status_code, 404)
        view = resolve('/')
        self.assertEquals(view.func, home_page)
        self.assertTemplateUsed(response, 'home.html')
