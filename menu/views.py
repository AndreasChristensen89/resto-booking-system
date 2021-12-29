from django.shortcuts import render, get_object_or_404
from .models import Category, Meals

# Create your views here.


def menu_list(request):
    menu_list = Meals.objects.all()
    categories = Category.objects.all()
    list_odd = [3, 7, 11, 15, 19]
    list_even= [4, 8, 12, 16, 20]

    context = {
        'menu_list': menu_list,
        'categories': categories,
        'list_odd': list_odd,
        'list_even': list_even,
    }

    return render(request, 'menu_list.html', context)
