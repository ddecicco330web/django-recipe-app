# Django imports
from django.test import TestCase

# App imports
from .forms import RecipesSearchForm
from .forms import RecipeForm

# RecipeFormTest: Tests the Recipe form
class RecipeFormTest(TestCase):
    # Test the Recipe form
    def test_recipe_search_form(self):
        form_data = {'recipe': 'Test Recipe', 'ingredient': 'Test Ingredient', 'difficulty': 'Easy'}
        form = RecipesSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    # Test the Recipe form with empty data
    def test_recipe_search_form_empty(self):
        form_data = {}
        form = RecipesSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    # Test the Recipe form with invalid recipe
    def test_recipe_search_form_invalid_recipe(self):
        form_data = {'recipe': 'Invalid Recipe', 'ingredient': 'Test Ingredient', 'difficulty': 'Easy'}
        form = RecipesSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    # Test the Recipe form with invalid ingredient
    def test_recipe_search_form_invalid_ingredient(self):
        form_data = {'recipe': 'Test Recipe', 'ingredient': 'Invalid Ingredient', 'difficulty': 'Easy'}
        form = RecipesSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    # Test the Recipe form with partial data
    def test_partial_recipe_search_form(self):
        form_data = {'recipe': 'Test Recipe'}
        form = RecipesSearchForm(data=form_data)
        self.assertTrue(form.is_valid())


class RecipeFormTest(TestCase):
    # Test the Add Recipe form
    def test_add_recipe_form(self):
        form_data = {'name': 'Test Recipe', 'description': 'Test Description', 'cook_time': 10, 'instructions': 'Test Instructions', 'ingredients': 'Test Ingredient'}
        form = RecipeForm(data=form_data)
        self.assertTrue(form.is_valid())

    # Test the Add Recipe form with empty data
    def test_add_recipe_form_empty(self):
        form_data = {}
        form = RecipeForm(data=form_data)
        self.assertFalse(form.is_valid())

    # Test the Add Recipe form with invalid data
    def test_add_recipe_form_invalid(self):
        form_data = {'name': 'Test Recipe' *100, 'description': 'Test Description', 'cook_time': 10, 'instructions': 'Test Instructions', 'ingredients': 'Test Ingredient'}
        form = RecipeForm(data=form_data)
        self.assertFalse(form.is_valid())

    # Test the Add Recipe form with invalid cook time
    def test_add_recipe_form_invalid_cook_time(self):
        form_data = {'name': 'Test Recipe', 'description': 'Test Description', 'cook_time': -1, 'instructions': 'Test Instructions', 'ingredients': 'Test Ingredient'}
        form = RecipeForm(data=form_data)
        self.assertFalse(form.is_valid())

