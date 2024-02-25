# Django imports
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, TemplateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Lower
from django.contrib.auth.mixins import LoginRequiredMixin

# App imports
from .models import Recipe
from recipe_ingredients.models import RecipeIngredient
from ingredients.models import Ingredient
from .forms import RecipesSearchForm
from .forms import RecipeForm
from .utils import get_chart

# Third-party imports
import pandas as pd


# Create your views here.
# home: Renders the home page for the recipes app
def home(request):
    return render(request, 'recipes/recipes_home.html')

# RecipeListView: Renders a list of all recipes
class RecipeListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'recipes/recipes_list.html'
    context_object_name = 'recipes'
    ordering = ['name']

# RecipeDetailView: Renders the details of a single recipe
class RecipeDetailView(LoginRequiredMixin, DetailView):
    model = Recipe
    template_name = 'recipes/recipes_detail.html'
    context_object_name = 'recipe'
    
    # get_context_data: Overrides the get_context_data method to add the ingredients to the context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe = self.object
        recipe.calculate_difficulty()
        recipe.save()
        
        # Retrieve ingredients for the current recipe
        ingredients = RecipeIngredient.objects.filter(recipe=self.object).order_by('ingredient__name')
        
        # Add ingredients to the context
        context['recipe_ingredients'] = ingredients
        
        return context
    
# records: Renders the records page for the recipes app
@login_required 
def records(request):
    form = RecipesSearchForm(request.POST or None)
    qs = None
    recipes_df = pd.DataFrame(Recipe.objects.all().values())
    chart = None

    if request.method == 'POST':
        form = RecipesSearchForm(request.POST)
        if form.is_valid():
            recipe = request.POST.get('recipe')
            ingredient = request.POST.get('ingredient')
            difficulty = request.POST.get('difficulty')
            
            # Filter recipes based on the recipe name
            if recipe:
                qs = Recipe.objects.filter(name__icontains=recipe)

            # Filter recipes based on the ingredient name
            if ingredient:
                ingredient = ingredient.lower()
                ingredient_query = RecipeIngredient.objects.filter(ingredient__name__icontains=ingredient).annotate(lower_name=Lower('ingredient__name')).values('recipe').distinct()
                if qs:
                    qs = qs.filter(id__in=ingredient_query)
                else:
                    qs = Recipe.objects.filter(id__in=ingredient_query)

            # Filter recipes based on the difficulty level
            if form.cleaned_data.get('difficulty') != 'Any':
                if qs:
                    qs = qs.filter(difficulty=difficulty)
                else:
                    qs = Recipe.objects.filter(difficulty=difficulty)
            elif qs is None:
                qs = Recipe.objects.all().values()
                    

            # Create a dataframe with the filtered recipes
            if qs:
                recipes_df = pd.DataFrame(qs.values())
            else:
                recipes_df = pd.DataFrame()

     
    if recipes_df.empty is False:
        difficulty = recipes_df['difficulty'].value_counts()
        chart=get_chart(difficulty, labels=recipes_df['difficulty'].unique())   
               
    context = {'form': form, 'recipes_df': recipes_df, 'chart': chart}      
    return render(request, 'recipes/records.html', context)

# ProfileView: Renders the user profile page for the recipes app       
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'recipes/profile.html'
    
   
    # get_context_data: Overrides the get_context_data method to add the current user to the context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['form'] = RecipeForm()
        context['recipes'] = Recipe.objects.filter(created_by=self.request.user)
        return context
    
    def post(self, request, *args, **kwargs):
        
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            print('valid')
            recipe = Recipe.objects.create(name=form.cleaned_data['name'], description=form.cleaned_data['description'], cook_time=form.cleaned_data['cook_time'], created_by=self.request.user, instructions=form.cleaned_data['instructions'])

            if form.cleaned_data['pic']:
                recipe.pic = form.cleaned_data['pic']
                recipe.save()
            
            recipe.calculate_difficulty()
            recipe.save()

            ingredients_input = form.cleaned_data['ingredients']
            ingredients_names = [name.strip() for name in ingredients_input.splitlines()]

            for name in ingredients_names:
                ingredient = Ingredient.objects.filter(name=name).first()
                if ingredient is None:
                    ingredient = Ingredient.objects.create(name=name)
                RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient)

            return redirect(request.path)
        else:
            context = self.get_context_data(form=form)
            context['form_errors'] = form.errors
            print(form.errors)
            return self.render_to_response(context)
        
# delete_recipe: Deletes a recipe
@login_required
def delete_recipe(request, pk):
    try:
        recipe = Recipe.objects.get(pk=pk)
    except Recipe.DoesNotExist:
        return HttpResponse(status=404)
    
    recipe.delete()
    return redirect('recipes:user-profile')

# UpdateRecipeView: Renders the update recipe page for the recipes app
class UpdateRecipeView(LoginRequiredMixin, UpdateView):
    template_name = 'recipes/update_recipe.html'
    form_class = RecipeForm
    queryset = Recipe.objects.all()
    success_url = '/update_success/'
    
    # get_initial: Overrides the get_initial method to add the ingredients to the initial form data
    def get_initial(self):
        initial = super().get_initial()
        recipe = self.get_object()
        # Get the list of ingredients associated with the recipe
        recipe_ingredients = RecipeIngredient.objects.filter(recipe=recipe)
        # Format the list of ingredients into a string
        ingredient_list = '\n'.join([recipe_ingredient.ingredient.name for recipe_ingredient in recipe_ingredients])
        # Set the formatted string as the initial value for the textarea
        initial['ingredients'] = ingredient_list
        return initial
    
    # form_valid: Overrides the form_valid method to update the recipe and ingredients
    def form_valid(self, form):
        form.instance.user = self.request.user

        # Get the current recipe instance
        recipe = self.get_object()

        # Save the recipe form to update recipe details
        recipe_form = form.save(commit=False)
        recipe_form.save()

        # Update ingredients
        ingredients_input = form.cleaned_data['ingredients']
        ingredients_names = [name.strip() for name in ingredients_input.splitlines()]
        
        RecipeIngredient.objects.filter(recipe=recipe).delete()

        # Create new ingredients
        for name in ingredients_names:
            ingredient = Ingredient.objects.filter(name=name).first()
            if ingredient is None:
                ingredient = Ingredient.objects.create(name=name)
            RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient)

        
        return super().form_valid(form)

    # form_invalid: Overrides the form_invalid method to handle invalid form submissions
    def form_invalid(self, form):
        
        self.object = self.get_object()
        context = self.get_context_data(form=form)
        context['form_errors'] = form.errors
        return self.render_to_response(context)
  
# about: Renders the about page for the recipes app
@login_required
def about(request):
    return render(request, 'recipes/about.html')

# update_success: Renders the update success page for the recipes app
@login_required
def update_success(request):
    return render(request, 'recipes/update_success.html')