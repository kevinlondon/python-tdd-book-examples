import logging
logger = logging.getLogger(__name__)
import requests
from django.contrib.auth import get_user_model
from django.conf import settings
User = get_user_model()

PERSONA_VERIFY_URL = 'https://verifier.login.persona.org/verify'


class PersonaAuthenticationBackend(object):

    def authenticate(self, assertion):
        data = {'assertion': assertion, 'audience': settings.DOMAIN}
        response = requests.post(PERSONA_VERIFY_URL, data=data)

        resp_data = response.json()
        if response.ok and resp_data['status'] == 'okay':
            email = resp_data['email']
            try:
                return User.objects.get(email=email)
            except User.DoesNotExist:
                return User.objects.create(email=email)
        else:
            logger.warning('Persona says no. Json was: {}'.format(resp_data))

    def get_user(self, email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
