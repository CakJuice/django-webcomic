from django.test import TestCase

from webcomic_site.base.forms import SignupForm


class SignupFormTests(TestCase):
    def test_form_has_fields(self):
        form = SignupForm()
        expected = ['username', 'email', 'password1', 'password2']
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)
