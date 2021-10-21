from django.urls import path
from . import views


urlpatterns = [
    path('', views.ReservationList.as_view(), name='home'),
    path('<slug:slug>/', views.ReservationDetail.as_view(), name='reservation_detail'),
    path('make_reservation/', views.reserve_table, name='make_reservation'),
]
