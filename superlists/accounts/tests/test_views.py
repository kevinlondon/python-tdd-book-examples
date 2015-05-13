from django.test import TestCase
from unittest.mock import patch


class LoginViewTest(TestCase):

    @patch('accounts.views.authenticate')
    def test_calls_authenticate_with_assertion_from_post(self, mock_auth):
        mock_auth.return_value = None
        self.client.post('/accounts/login', {'assertion': 'assert this'})
        mock_auth.assert_called_once_with(assertion='assert this')
