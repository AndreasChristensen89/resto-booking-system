from django.urls import path
from . import views


app_name = 'bookings'

urlpatterns = [
    path('', views.BookingList.as_view(), name='booking_list'),
    path('check_availability/', views.CheckAvailability.as_view(), name='check_availability'),
    path('book_table/', views.book_table, name='book_table'),
    path('<slug:slug>/', views.BookingDetail.as_view(), name='booking_detail'),
    path('<slug:slug>/cancel/', views.CancelBookingView.as_view(), name='cancel_booking'),
    path('<slug:slug>/update/', views.UpdateReservationView.as_view(), name='update_booking'),
]
