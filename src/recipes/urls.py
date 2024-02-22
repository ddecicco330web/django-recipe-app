from django.urls import path
from .views import home, RecipeListView, RecipeDetailView, records, ProfileView, delete_recipe, UpdateRecipeView, about, update_success

app_name = 'recipes'
urlpatterns = [
   path('', home),
   path('recipes/', RecipeListView.as_view(), name='recipes-list'),
   path('recipes/<pk>/', RecipeDetailView.as_view(), name='recipes-detail'),
   path('search/', records, name='records-search'),
   path('profile/', ProfileView.as_view(), name='user-profile'),
   path('profile/<pk>/delete/', delete_recipe, name='delete-recipe'),
   path('profile/<pk>/update/', UpdateRecipeView.as_view(), name='update-recipe'),
   path('about/', about, name='about'),
   path('update_success/', update_success, name='update-success')
]
