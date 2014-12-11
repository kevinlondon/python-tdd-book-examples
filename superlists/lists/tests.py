from django.test import TestCase

class SmokeTest(TestCase):

    def test_bad_maths(self):
        assert 1+1 == 3
