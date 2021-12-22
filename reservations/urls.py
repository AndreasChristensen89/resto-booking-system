from django.urls import path
from . import views


app_name = 'reservations'

urlpatterns = [
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('password/', views.PasswordChangeView.as_view(), name='password'),
    path('bookings/', views.BookingList.as_view(), name='booking_list'),
    path('previous_bookings/', views.BookingListPrevious.as_view(), name='booking_list_previous'),
    path('book_table/', views.book_table, name='book_table'),
    path('updated/', views.BookingUpdated.as_view(), name='bookings_updated'),
    path('pending/', views.BookingPending.as_view(), name='bookings_pending'),
    path('<slug:slug>/', views.BookingDetail.as_view(), name='booking_detail'),
    path('<slug:slug>/cancel/', views.CancelBookingView.as_view(), name='cancel_booking'),
    path('<slug:slug>/update/', views.UpdateReservationView.as_view(), name='update_booking'),
    path('<slug:slug>/update_admin/', views.UpdateReservationViewAdmin.as_view(), name='admin_update_booking'),
    path('<slug:slug>/approve_booking/', views.ApproveReservationViewAdmin.as_view(), name='approve_booking'),
]
