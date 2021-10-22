from django.contrib import admin
from .models import Category, Meals


@admin.register(Meals)
class MealsAdmin(admin.ModelAdmin):

    list_display = ('name', 'category')
    search_fields = ['name', 'category', 'for_nbr_people', 'price']
    list_filter = ('category', 'for_nbr_people', 'price')


admin.site.register(Category)
