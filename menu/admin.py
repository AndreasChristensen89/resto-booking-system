from django.contrib import admin
from .models import Category, Meals
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Meals)
class MealsAdmin(SummernoteModelAdmin):

    summernote_fields = ('description')
    list_display = ('name', 'category')
    search_fields = ['name', 'category', 'for_nbr_people', 'price']
    list_filter = ('category', 'for_nbr_people', 'price')


admin.site.register(Category)
