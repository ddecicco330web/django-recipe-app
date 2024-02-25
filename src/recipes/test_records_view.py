# Django imports
from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client

# App imports
from .models import Recipe
from recipe_ingredients.models import RecipeIngredient
from ingredients.models import Ingredient

# RecipeRecordsViewTest: Tests the Recipe records view
class RecipeRecordsViewTest(TestCase):
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

    # Test the Recipe records view redirect to login
    def test_recipe_records_view_redirect_to_login(self):
        # this client isn't logged in
        response = self.client.get('/search/')
        self.assertEqual(response.status_code, 302)

    # Test the Recipe records view
    def test_recipe_records_view(self):
        response = self.c.get('/search/')
        self.assertEqual(response.status_code, 200)

    # Test the Recipe records view post method
    def test_recipe_records_view_post(self):
        response = self.c.post('/search/', {'recipe': 'Test Recipe', 'ingredient': 'Test Ingredient', 'difficulty': 'Easy'})
        self.assertEqual(response.status_code, 200)

    # Test the Recipe records view post method with invalid data
    def test_recipe_records_view_post_invalid(self):
        response = self.c.post('/search/', {'recipe': 'Invalid Recipe', 'ingredient': 'Invalid Ingredient', 'difficulty': 'Easy'})
        self.assertEqual(response.status_code, 200)

    # Test the Recipe records view post method with partial data
    def test_recipe_records_view_post_partial(self):
        response = self.c.post('/search/', {'recipe': 'Test Recipe'})
        self.assertEqual(response.status_code, 200)

    # Test the Recipe records view post method with only ingredient
    def test_recipe_records_view_post_partial_ingredient(self):
        response = self.c.post('/search/', {'ingredient': 'Test Ingredient'})
        self.assertEqual(response.status_code, 200)

    # Test the Recipe records view post method with only difficulty
    def test_recipe_records_view_post_partial_difficulty(self):
        response = self.c.post('/search/', {'difficulty': 'Easy'})
        self.assertEqual(response.status_code, 200)

    # Test the Recipe records view context
    def test_context(self):
        response = self.c.get('/search/')
        self.assertTrue('form' in response.context)
        self.assertTrue('recipes_df' in response.context)
        self.assertTrue('chart' in response.context)