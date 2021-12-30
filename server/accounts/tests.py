from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User


class AccountsViewTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()
