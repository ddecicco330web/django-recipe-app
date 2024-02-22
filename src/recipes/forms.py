from django import forms
from .models import Recipe

difficulty_choices = [
    ('Any', 'Any'),
    ('Easy', 'Easy'),
    ('Medium', 'Medium'),
    ('Intermediate', 'Intermediate'),
    ('Hard', 'Hard')
]

class RecipesSearchForm(forms.Form):
    recipe = forms.CharField(label='Recipe', max_length=100, required=False)
    ingredient = forms.CharField(label='Ingredient', max_length=100, required=False)
    difficulty = forms.ChoiceField(label='Difficulty', choices=difficulty_choices, required=False)


  
class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'description', 'cook_time', 'instructions', 'ingredients', 'pic']
    name = forms.CharField(label='Name', max_length=50)
    description = forms.CharField(label='Description', widget=forms.Textarea(attrs={'class': 'fixed-text-field'}))
    cook_time = forms.IntegerField(label='Cook Time (min)')
    ingredients = forms.CharField(label='Ingredients', widget=forms.Textarea(attrs={'class': 'fixed-text-field'}))
    instructions = forms.CharField(label='Instructions', widget=forms.Textarea(attrs={'class': 'fixed-text-field'}))
    pic = forms.ImageField(label='Picture', required=False, widget=forms.FileInput)


    def clean_cook_time(self):
        data = self.cleaned_data['cook_time']
        if data is not None and data < 0:
            raise forms.ValidationError("Enter a positive number")
        return data