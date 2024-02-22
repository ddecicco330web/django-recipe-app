# Django imports
from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client

class AboutViewTest(TestCase):
    # Login and create Recipe and Ingredient objects for testing
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.is_active = True
        user.save()

        cls.c = Client()
        cls.c.login(username='testuser', password='12345')

   # Test the About view
    def test_about_view(self):
        response = self.c.get('/about/')
        self.assertEqual(response.status_code, 200)

    # Test the About view redirect to login
    def test_about_view_redirect_to_login(self):
        # this client isn't logged in
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 302)