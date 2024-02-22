# Django imports
from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client

# App imports
from .models import Recipe
from recipe_ingredients.models import RecipeIngredient
from ingredients.models import Ingredient

class UpdateRecipeView(TestCase):
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

    # Test the Recipe update view redirect to login
    def test_recipe_update_view_redirect_to_login(self):
        # this client isn't logged in
        response = self.client.get('/profile/1/update/')
        self.assertEqual(response.status_code, 302)

    # Test the Recipe update view
    def test_recipe_update_view(self):
        response = self.c.get('/profile/1/update/')
        self.assertEqual(response.status_code, 200)

    # Test the Recipe update view invalid
    def test_recipe_update_view_invalid(self):
        response = self.c.get('/profile/2/update/')
        self.assertEqual(response.status_code, 404)

    # Test the Recipe update view post method
    def test_recipe_update_view_post(self):
        response = self.c.post('/profile/1/update/', {'name': 'Test Recipe', 'description': 'Test Description', 'cook_time': 10, 'ingredients': 'Test Ingredient', 'instructions': 'Test Instructions', 'difficulty': 'Easy'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/update_success/')

    # Test the Recipe update view post method with invalid data
    def test_recipe_update_view_post_invalid(self):
        response = self.c.post('/profile/1/update/', {'name': 'Test Recipe', 'description': 'Test Description', 'cook_time': -1, 'ingredients': 'Test Ingredient', 'instructions': 'Test Instructions', 'difficulty': 'Easy'})
        self.assertEqual(response.status_code, 200)


    