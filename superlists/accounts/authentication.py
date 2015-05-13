import requests
from django.contrib.auth import get_user_model
User = get_user_model()

PERSONA_VERIFY_URL = 'https://verifier.login.persona.org/verify'
DOMAIN = 'localhost'


class PersonaAuthenticationBackend(object):

    def authenticate(self, assertion):
        data = {'assertion': assertion, 'audience': DOMAIN}
        response = requests.post(PERSONA_VERIFY_URL, data=data)

        resp_data = response.json()
        if response.ok and resp_data['status'] == 'okay':
            return User.objects.get(email=resp_data['email'])