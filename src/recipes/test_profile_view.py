# Django imports
from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client

# App imports
from .models import Recipe
from recipe_ingredients.models import RecipeIngredient
from ingredients.models import Ingredient

# ProfileViewTest: Tests the profile view
class ProfileViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='testuser')
        cls.user.set_password('12345')
        cls.user.is_active = True
        cls.user.save()

        cls.c = Client()
        cls.c.login(username='testuser', password='12345')
        
        Recipe.objects.create(name="Test Recipe", description="Test Description", cook_time=10)

    # Test the profile view redirect to login
    def test_profile_view_redirect_to_login(self):
        # this client isn't logged in
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 302)
    
    # Test the profile view
    def test_profile_view(self):
        response = self.c.get('/profile/')
        self.assertEqual(response.status_code, 200)

    # Test get query set
    def test_get_queryset(self):
        response = self.c.get('/profile/')
        self.assertEqual(response.context['recipes'][0].created_by, self.user)

    # Test get context data
    def test_get_context_data(self):
        response = self.c.get('/profile/')
        self.assertEqual(response.context['user'].username, 'testuser')


