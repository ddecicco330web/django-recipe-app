# Django imports
from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client

# App imports
from .models import Recipe
from .forms import RecipesSearchForm
from recipe_ingredients.models import RecipeIngredient
from ingredients.models import Ingredient


# Create your tests here.
# RecipeModelTest: Tests the Recipe model
class RecipeModelTest(TestCase):
    # Create Recipe object for testing
    def setUpTestData():
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.is_active = True
        user.save()

        Recipe.objects.create(name="Test Recipe", description="Test Description", cook_time=10, difficulty="Easy")

    # Test Fields
    # Test the name field
    def test_recipe_name(self):
        recipe = Recipe.objects.get(id=1)
        field_label = recipe._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    # Test the instructions field
    def test_recipe_instructions(self):
        recipe = Recipe.objects.get(id=1)
        field_label = recipe._meta.get_field('instructions').verbose_name
        self.assertEqual(field_label, 'instructions')

    # Test cook time field
    def test_recipe_cook_time(self):
        recipe = Recipe.objects.get(id=1)
        field_label = recipe._meta.get_field('cook_time').verbose_name
        self.assertEqual(field_label, 'cook time')

    # Test difficulty field
    def test_recipe_difficulty(self):
        recipe = Recipe.objects.get(id=1)
        field_label = recipe._meta.get_field('difficulty').verbose_name
        self.assertEqual(field_label, 'difficulty')

    # Test the pic field
    def test_recipe_pic(self): 
        recipe = Recipe.objects.get(id=1)
        field_label = recipe._meta.get_field('pic').verbose_name
        self.assertEqual(field_label, 'pic')

    # Test Max Lengths
    # Test the name field max length
    def test_recipe_name_max_length(self):
        recipe = Recipe.objects.get(id=1)
        max_length = recipe._meta.get_field('name').max_length
        self.assertEqual(max_length, 50)
    
    # Test difficulty field max length
    def test_recipe_difficulty_max_length(self):
        recipe = Recipe.objects.get(id=1)
        max_length = recipe._meta.get_field('difficulty').max_length
        self.assertEqual(max_length, 20)

    # Test Methods
    # Test the __str__ method
    def test_recipe_str_method(self):
        recipe = Recipe.objects.get(id=1)
        expected_object_name = "Name: Test Recipe, Description: Test Description, Cook Time (min): 10, Difficulty: Easy"
        self.assertEqual(expected_object_name, str(recipe))

    # Test the get_absolute_url method
    def test_get_absolute_url(self):
       recipe = Recipe.objects.get(id=1)
       self.assertEqual(recipe.get_absolute_url(), '/recipes/1/')

    # Test the calculate_difficulty method
    def test_calculate_difficulty(self):
        recipe = Recipe.objects.get(id=1)
        recipe.calculate_difficulty()
        self.assertTrue((recipe.difficulty in ['Easy', 'Medium', 'Intermediate', 'Hard']))

    

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
