from django.urls import path
from . import views


app_name = 'bookings'

urlpatterns = [
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('password/', views.PasswordChangeView.as_view(), name='password'),
    path('resetpassword/', views.PasswordChangeView.as_view(), name='password'),
    path('', views.BookingList.as_view(), name='booking_list'),
    path('book_table/', views.book_table, name='book_table'),
    path('updated_bookings/', views.BookingsUpdated.as_view(), name='updated_list'),
    path('pending_bookings/', views.BookingsPending.as_view(), name='pending_bookings'),
    path('<slug:slug>/', views.BookingDetail.as_view(), name='booking_detail'),
    path('<slug:slug>/cancel/', views.CancelBookingView.as_view(), name='cancel_booking'),
    path('<slug:slug>/update/', views.UpdateReservationView.as_view(), name='update_booking'),
    path('<slug:slug>/adminupdate/', views.UpdateReservationViewAdmin.as_view(), name='update_booking_admin'),
    path('<slug:slug>/approve_booking/', views.ApproveReservationViewAdmin.as_view(), name='approve_booking'),
]
