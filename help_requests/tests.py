from django.contrib.auth import get_user_model
from django.test import TestCase

class HelpRequestTestCase(TestCase):
    def setUp(self):
        self.hr = HelpRequest(title)
        self.user = get_user_model().objects.create_user('testuser')

    def tearDown(self):
        self.hr.delete()
        self.user.delete()
