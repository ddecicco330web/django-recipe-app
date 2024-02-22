from django.db import models
from recipes.models import Recipe
from ingredients.models import Ingredient

# Create your models here.
class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    def __str__(self):
        return f"Recipe: {self.recipe.name}, Ingredient: {self.ingredient.name}"