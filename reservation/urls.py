from . import views
from django.urls import path


urlpatterns = [
    path('', views.ReservationList.as_view(), name='home'),
    path('<slug:slug>/', views.ReservationDetail.as_view(), name='reservation_detail'),
]
