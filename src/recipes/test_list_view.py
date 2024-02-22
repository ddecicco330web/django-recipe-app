# Django imports
from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client

# App imports
from .models import Recipe

# RecipeListViewTest: Tests the Recipe list view
class RecipeListViewTest(TestCase):
    # Login and create Recipe and Ingredient objects for testing
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.is_active = True
        user.save()

        cls.c = Client()
        cls.c.login(username='testuser', password='12345')
        
        Recipe.objects.create(name="Test Recipe", description="Test Description", cook_time=10)

    # Test the Recipe list view redirect to login
    def test_recipe_list_view_redirect_to_login(self):
        # this client isn't logged in
        response = self.client.get('/recipes/')
        self.assertEqual(response.status_code, 302)

    # Test the Recipe list view
    def test_recipe_list_view(self):
        response = self.c.get('/recipes/')
        self.assertEqual(response.status_code, 200)