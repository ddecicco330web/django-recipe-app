# Django imports
from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client

# App imports
from .models import Recipe
from recipe_ingredients.models import RecipeIngredient
from ingredients.models import Ingredient

# RecipeDetailViewTest: Tests the Recipe detail view
class RecipeDetailViewTest(TestCase):
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
        Ingredient.objects.create(name="Test Ingredient")
        RecipeIngredient.objects.create(recipe=Recipe.objects.get(id=1), ingredient=Ingredient.objects.get(id=1))

    # Test the Recipe detail view redirect to login
    def test_recipe_detail_view_redirect_to_login(self):
        # this client isn't logged in
        response = self.client.get('/recipes/1/')
        self.assertEqual(response.status_code, 302)

    # Test the Recipe detail view
    def test_recipe_detail_view(self):
        response = self.c.get('/recipes/1/')
        self.assertEqual(response.status_code, 200)

    # Test the Recipe detail view invalid
    def test_recipe_detail_view_invalid(self):
        response = self.c.get('/recipes/2/')
        self.assertEqual(response.status_code, 404)

    # Test the Recipe detail view context
    def test_get_context_data(self):
        response = self.c.get('/recipes/1/')
        self.assertEqual(response.context['recipe'].name, 'Test Recipe')

    # Test the Recipe detail view context ingredients
    def test_get_context_data_ingredients(self):
        response = self.c.get('/recipes/1/')
        self.assertEqual(response.context['recipe_ingredients'][0].ingredient.name, 'Test Ingredient')

    # Test the Recipe detail view context difficulty
    def test_get_context_data_difficulty(self):
        response = self.c.get('/recipes/1/')
        self.assertTrue(response.context['recipe'].difficulty in ['Easy', 'Medium', 'Intermediate', 'Hard'])
        