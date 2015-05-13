from django.contrib.auth import get_user_model, SESSION_KEY
from django.test import TestCase
from unittest.mock import patch
User = get_user_model()


class LoginViewTest(TestCase):

    @patch('accounts.views.authenticate')
    def test_calls_authenticate_with_assertion_from_post(self, mock_auth):
        mock_auth.return_value = None
        self.client.post('/accounts/login', {'assertion': 'assert this'})
        mock_auth.assert_called_once_with(assertion='assert this')

    @patch('accounts.views.authenticate')
    def test_returns_ok_when_user_found(self, mock_auth):
        user = User.objects.create(email='a@b.com')
        user.backend = ''  # required for auth_login to work
        mock_auth.return_value = user
        response = self.client.post('/accounts/login', {'assertion': 'a'})
        assert response.content.decode() == 'OK'

    @patch('accounts.views.authenticate')
    def test_gets_logged_in_session_if_auth_returns_a_user(self, mock_auth):
        user = User.objects.create(email='a@b.com')
        user.backend = ''  # required for auth_login to work
        mock_auth.return_value = user
        response = self.client.post('/accounts/login', {'assertion': 'a'})
        assert self.client.session[SESSION_KEY] == user.pk

    @patch('accounts.views.authenticate')
    def test_does_not_get_logged_in_if_auth_returns_none(self, mock_auth):
        mock_auth.return_value = None
        self.client.post('/accounts/login', {'assertion': 'a'})
        assert SESSION_KEY not in self.client.session
