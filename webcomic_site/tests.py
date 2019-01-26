from django.contrib.auth.models import User
from django.test import TestCase


class BaseTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='juice', email='test@email.com', password='test')
