from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserModelTest(TestCase):

    def test_user_is_valid_with_email_only(self):
        user = User(email='a@b.com')
        user.full_clean()   # Should not raise an error

    def test_email_is_primary_key(self):
        user = User()
        assert hasattr(user, 'id') is False

    def test_is_authenticated(self):
        user = User()
        assert user.is_authenticated()
