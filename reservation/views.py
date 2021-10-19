from django.shortcuts import render
from django.views import generic
from .models import Reservation


class ReservationList(generic.ListView):
    model = Reservation
    queryset = Reservation.objects.all()
    template_name = 'index.html'
    paginate_by = 9
