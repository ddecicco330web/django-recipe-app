from django.contrib import admin
from .models import RecipeIngredient

# Register your models here.
@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient')
    list_filter = ('recipe__name', 'ingredient__name')
    ordering = ('recipe__name', 'ingredient__name')
    search_fields = ('recipe__name', 'ingredient__name')

