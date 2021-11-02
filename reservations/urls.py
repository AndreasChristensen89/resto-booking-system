from django.urls import path
from . import views


app_name = 'reservations'

urlpatterns = [
    path('<slug:slug>/', views.ReservationDetail.as_view(), name='reservation_detail'),
    path('reserve_table/', views.reserve_table, name='reserve_table'),
    path('<slug:slug>/cancel/', views.CancelReservationView.as_view(), name='cancel_reservation'),
    path('<slug:slug>/update/', views.UpdateReservationView.as_view(), name='update_reservation'),
    path('', views.ReservationList.as_view(), name='reservation_list'),
]
