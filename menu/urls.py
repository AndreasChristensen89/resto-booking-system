from django.urls import path
from . import views


urlpatterns = [
    path('', views.menu_list, name='menu_list'),
    path('<slug:slug>/', views.meal_detail, name='meal_detail'),
]
