from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth import get_user_model
User = get_user_model()

from accounts.authentication import (
    PERSONA_VERIFY_URL, DOMAIN, PersonaAuthenticationBackend
)


@patch('accounts.authentication.requests.post')
class AuthenticateTest(TestCase):

    def setUp(self):
        self.backend = PersonaAuthenticationBackend()
        user = User(email='other@user.com')
        user.username = 'otheruser'
        user.save()

    def test_sends_assertion_to_mozilla_with_domain(self, mock_post):
        self.backend.authenticate('an assertion')
        data = {'assertion': 'an assertion', 'audience': DOMAIN}
        mock_post.assert_called_once_with(PERSONA_VERIFY_URL, data=data)

    def test_returns_none_if_response_errors(self, mock_post):
        mock_post.return_value.ok = False
        mock_post.return_value.json.return_value = {}
        user = self.backend.authenticate('an assertion')
        assert user is None

    def test_returns_none_if_status_not_ok(self, mock_post):
        mock_post.return_value.json.return_value = {'status': 'not okay'}
        user = self.backend.authenticate('an assertion')
        assert user is None

    def test_finds_existing_user_with_email(self, mock_post):
        data = {'status': 'okay', 'email': 'a@b.com'}
        mock_post.return_value.json.return_value = data
        actual_user = User.objects.create(email='a@b.com')
        found_user = self.backend.authenticate('an assertion')
        assert found_user == actual_user

    def test_creates_new_user_if_necessary_for_valid_assertion(self, mock_post):
        mock_post.return_value.json.return_value = {'status': 'okay', 'email': 'a@b.com'}
        found_user = self.backend.authenticate('an assertion')
        new_user = User.objects.get(email='a@b.com')
        assert found_user == new_user
