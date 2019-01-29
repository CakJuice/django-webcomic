from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve

from webcomic_site.base import views
from webcomic_site.base.forms import SignupForm
from webcomic_site.base.models import UserActivation


class SignupTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.get(url)

    def test_signup_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_signup_url_resolves_signup_view(self):
        view = resolve('/signup/')
        self.assertEqual(view.func, views.signup)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, SignupForm)

    def test_form_input(self):
        # The view must contain five inputs: csrf, username, email, password1, password2
        self.assertContains(self.response, '<input', 5)
        self.assertContains(self.response, 'type="text"', 1)
        self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, 'type="password"', 2)


class BaseSignup(TestCase):
    def setUp(self):
        url = reverse('signup')
        data = {
            'username': 'juice',
            'email': 'juice@test.com',
            'password1': 'test123456',
            'password2': 'test123456',
        }
        self.response = self.client.post(url, data)
        self.success_url = reverse('signup_success', kwargs={'username': data['username']})


class SuccessfulSignupTests(BaseSignup):
    def test_redirection(self):
        self.assertRedirects(self.response, self.success_url)

    def test_user_creation(self):
        self.assertTrue(User.objects.exists())

    def test_user_not_active(self):
        user = User.objects.get(username='juice')
        self.assertFalse(user.is_active)


class SuccessfulUserActivation(BaseSignup):
    def test_user_activation_creation_after_signup(self):
        self.assertTrue(UserActivation.objects.exists())


class InvalidSignupTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.post(url, {})  # submit an empty dictionary

    def test_signup_status_code(self):
        """An invalid form submission should return to the same page
        """
        self.assertEqual(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_dont_create_user(self):
        self.assertFalse(User.objects.exists())
