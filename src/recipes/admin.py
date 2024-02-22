from django.contrib import admin
from .models import Recipe

# Register your models here.
@admin.register(Recipe)

class RecipeAdmin(admin.ModelAdmin):
    ordering = ('name',)
    search_fields = ('name',)
