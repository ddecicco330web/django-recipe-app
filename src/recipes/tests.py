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
        Ingredient.objects.create(name="Test Ingredient")
        RecipeIngredient.objects.create(recipe=Recipe.objects.get(id=1), ingredient=Ingredient.objects.get(id=1))

    # Test the Recipe list view redirect to login
    def test_recipe_list_view_redirect_to_login(self):
        # this client isn't logged in
        response = self.client.get('/recipes/')
        self.assertEqual(response.status_code, 302)

    # Test the Recipe list view
    def test_recipe_list_view(self):
        response = self.c.get('/recipes/')
        self.assertEqual(response.status_code, 200)

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
        self.assertTrue('charts' in response.context)