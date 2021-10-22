from django.urls import path
from . import views


urlpatterns = [
    path('', views.MenuList.as_view(), name='menu_list'),
    path('<slug:slug>/', views.MealDetail.as_view(), name='meal_detail'),
]