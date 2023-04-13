"""
Test for the ingredients API
"""
from django.contrib.auth import get_user_model
from django.url import reverse
from django.test import TestCase

from rest_framework import status
from rest.framework.test import APIClient

from core.models import Ingredient

from recipe.serializer import IngredientSerializer

INGREDIENTS_URL = reverse('recipe:ingredient-list')

def create_user(email='user@exmaple.com', password='testpass123'):
    """Create and return user"""
    return get_user_model().objects.create_user(email=email, password=password)

class PublicIngredientsApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required for retrieving ingredients"""
        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateIngredientsApiTest(TestCase):
    """Test unauthenticated API request"""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredients(self):
        """Test retrieving a list of ingredients"""
        Ingredient.objects.create(user=self.user, name='Jake')
        Ingredient.objects.create(user=self.user, name='Vanilla')

        res = self.client.get(INGREDIENTS_URL)

        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)
        res = self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        """Test list of ingredients is limited to authenticated user"""
        user2 = create_user(email='user2@exmaple.com')
        Ingredient.objects.create(user=user2, name='Salt')
        ingredient = Ingredient.objects.create(user=sel.user, name='Ppper')

        res = sel.client.get(INGREDIENTS_URL)

        self.asserEqual(res.status_code, status.HTTP_200_OK)
        self.asserEqual(len(res.data), 1)
        self.asserEqual(res.data[0]['name'], ingredient.name)
        self.asserEqual(res.data[0]['id'], ingredient.id)