# Django imports
from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client

# App imports
from .models import Recipe

class DeleteRecipeViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.is_active = True
        user.save()

        cls.c = Client()
        cls.c.login(username='testuser', password='12345')
        
        Recipe.objects.create(name="Test Recipe", description="Test Description", cook_time=10)

    # Test the Recipe delete view redirect to login
    def test_recipe_delete_view_redirect_to_login(self):
        # this client isn't logged in
        response = self.client.get('/profile/1/delete/')
        self.assertEqual(response.status_code, 302)
    
    # Test the Recipe delete view
    def test_recipe_delete_view(self):
        response = self.c.get('/profile/1/delete/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/profile/')


    # Test the Recipe delete view invalid
    def test_recipe_delete_view_invalid(self):
        response = self.c.get('/profile/2/delete/')
        self.assertEqual(response.status_code, 404)

 
    # Test if recipe is deleted
    def test_recipe_delete_view_deleted(self):
        response = self.c.get('/profile/1/delete/')
        self.assertEqual(Recipe.objects.filter(id=1).exists(), False)
    