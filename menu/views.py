from django.shortcuts import render, get_object_or_404
from .models import Category, Meals
from django.views import generic, View

# Create your views here.


class MenuList(generic.ListView):
    model = Meals, Category
    queryset_meals = Meals.objects.all()
    queryset_categories = Category.objects.all()
    template_name = 'menu_list.html'


class MealDetail(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Meals.objects.all()
        meal = get_object_or_404(queryset, slug=slug)

        return render(
            request,
            'meal_detail.html',
            {
                'meal': meal,
            }
        )
