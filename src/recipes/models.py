from django.db import models
from django.shortcuts import reverse


difficulty_choices =[('Easy', 'Easy'), ('Medium', 'Medium'), ('Intermediate', 'Intermediate'), ('Hard', 'Hard')]

# Create your models here.
class Recipe(models.Model):
    name = models.CharField(max_length=50)
    cook_time = models.PositiveIntegerField(help_text="In minutes")
    instructions = models.TextField()
    description = models.TextField()
    difficulty = models.CharField(max_length=20, choices = difficulty_choices, default='Easy')
    pic = models.ImageField(upload_to='recipe_pics', default='default.jpg')
    created_by = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='recipes', default=1)

    def __str__(self):
        return f"Name: {self.name}, Description: {self.description}, Cook Time (min): {self.cook_time}, Difficulty: {self.difficulty}"

    def get_absolute_url(self):
       return reverse ('recipes:recipes-detail', kwargs={'pk': self.pk})
    
    def get_delete_url(self):
        return reverse('recipes:delete-recipe', kwargs={'pk': self.pk})
    
    def get_update_url(self):
        return reverse('recipes:update-recipe', kwargs={'pk': self.pk})
    
    def calculate_difficulty(self):
        from recipe_ingredients.models import RecipeIngredient
        MAX_EASY_TIME = 10
        MAX_EASY_INGREDIENTS = 4

        ingredients = RecipeIngredient.objects.filter(recipe=self)

        self.difficulty = "Hard"
        if(self.cook_time < MAX_EASY_TIME and len(ingredients) < MAX_EASY_INGREDIENTS):
            self.difficulty = "Easy"
        elif(self.cook_time < MAX_EASY_TIME):
            self.difficulty = "Medium"
        elif(len(ingredients) < MAX_EASY_INGREDIENTS):
            self.difficulty = "Intermediate"

   


    