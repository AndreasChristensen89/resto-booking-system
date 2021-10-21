from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from .models import Reservation


class ReservationList(generic.ListView):
    model = Reservation
    queryset = Reservation.objects.all()
    template_name = 'index.html'
    paginate_by = 6


class ReservationDetail(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Reservation.objects.all()
        reservation = get_object_or_404(queryset, slug=slug)

        return render(
            request,
            'reservation_detail.html',
            {
                "reservation": reservation,
            }
            )
