from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from django.http import HttpResponseRedirect
from reservation.models import Reservation
from .forms import ReserveTableForm


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


# def reserve_table(request):

#     if request.method == 'POST':
#         form = ReserveTableForm(request.POST)

#         if form.is_valid():
#             reserve_form.save()

#     else:
#         form = ReserveTableForm()

#     return render(request, 'make_reservation.html', {'form': form})


def reserve_table(request):
 
    if request.method == 'POST':
        form = ReserveTableForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/thanks/')

    else:
        form = ReserveTableForm()

    return render(request, 'make_reservation.html', {'form': form})
