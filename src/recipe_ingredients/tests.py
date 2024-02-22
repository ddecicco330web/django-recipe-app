# Django imports
from django.test import TestCase
from django.contrib.auth.models import User

# App imports
from .models import RecipeIngredient
from recipes.models import Recipe
from ingredients.models import Ingredient

# Create your tests here.
# RecipeIngredientModelTest: Tests the RecipeIngredient model
class RecipeIngredientModelTest(TestCase):
    # Create RecipeIngredient object for testing
    def setUpTestData():
        User.objects.create(username='testuser')
        Recipe.objects.create(name="Test Recipe", description="Test Description", cook_time=10, difficulty="Easy")
        Ingredient.objects.create(name="Test Ingredient")
        RecipeIngredient.objects.create(recipe=Recipe.objects.get(id=1), ingredient=Ingredient.objects.get(id=1))

    # Test Fields
    def test_ri_recipe(self):
        recipe_ingredient = RecipeIngredient.objects.get(id=1)
        field_label = recipe_ingredient._meta.get_field('recipe').verbose_name
        self.assertEqual(field_label, 'recipe')

    def test_ri_ingredient(self):
        recipe_ingredient = RecipeIngredient.objects.get(id=1)
        field_label = recipe_ingredient._meta.get_field('ingredient').verbose_name
        self.assertEqual(field_label, 'ingredient')

    # Test the str method
    def test_ri_str_method(self):
        recipe_ingredient = RecipeIngredient.objects.get(id=1)
        expected_object_name = "Recipe: Test Recipe, Ingredient: Test Ingredient"
        self.assertEqual(expected_object_name, str(recipe_ingredient))