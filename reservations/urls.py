from django.urls import path
from . import views


app_name = 'reservations'

urlpatterns = [
    path('', views.ReservationList.as_view(), name='reservation_list'),
    path('reserve_table/', views.reserve_table, name='reserve_table'),
    path('<slug:slug>/', views.ReservationDetail.as_view(), name='reservation_detail'),
]
