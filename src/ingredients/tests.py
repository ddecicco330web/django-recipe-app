from django.test import TestCase
from .models import Ingredient

# Create your tests here.
class IngredientModelTests(TestCase):
    def setUpTestData():
        Ingredient.objects.create(name="Test Ingredient")

    def test_ingredient_name(self):
        ingredient = Ingredient.objects.get(id=1)
        field_label = ingredient._meta.get_field('name').verbose_name
        self.assertEqual(field_label, "name")

    def test_ingredient_name_max_length(self):
        ingredient = Ingredient.objects.get(id=1)
        max_length = ingredient._meta.get_field('name').max_length
        self.assertEqual(max_length, 50)

    def test_ingredient_str_method(self):
        ingredient = Ingredient.objects.get(id=1)
        expected_object_name = "Name: Test Ingredient"
        self.assertEqual(expected_object_name, str(ingredient))