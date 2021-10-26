from django.shortcuts import render, get_object_or_404
from .models import Category, Meals

# Create your views here.


def menu_list(request):
    menu_list = Meals.objects.all()
    categories = Category.objects.all()

    context = {
        'menu_list': menu_list,
        'categories': categories,
    }

    return render(request, 'menu_list.html', context)


def meal_detail(request, slug):
    meal_detail = Meals.objects.get(slug=slug)

    context = {'meal_detail': meal_detail}

    return render(request, 'meal_detail.html', context)
