from django.shortcuts import render, get_object_or_404
from .models import Category, Meals


def menu_list(request):
    breakfast = Meals.objects.filter(category__name="Breakfast")
    lunch = Meals.objects.filter(category__name="Lunch")
    dinner = Meals.objects.filter(category__name="Dinner")
    categories = Category.objects.all()

    context = {
        'breakfast': breakfast,
        'lunch': lunch,
        'dinner': dinner,
        'categories': categories,
    }

    return render(request, 'menu_list.html', context)
