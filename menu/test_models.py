from django.test import TestCase
from .models import Meals, Category

class TestModels(TestCase):
    
    def test_meals_object_exists(self):
        meal = Meals.objects.create(
            name='x',
            description='x', 
            for_nbr_people=2, 
            price=19)
        self.assertEqual(len(Meals.objects.filter(name='x')), 1)

    def test_category_object_exists(self):
        category = Category.objects.create(
            name='x')
        self.assertEqual(len(Category.objects.filter(name='x')), 1)
