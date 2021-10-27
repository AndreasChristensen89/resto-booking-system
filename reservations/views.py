from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from django.http import HttpResponseRedirect
from reservations.models import Reservations
from .forms import ReserveTableForm


def reserve_table(request):
    reserve_form = ReserveTableForm()

    if request.method == 'POST':
        reserve_form = ReserveTableForm(request.POST)

        if reserve_form.is_valid():
            reserve_form.save()
            HttpResponseRedirect('/')

    else:
        reserve_form = ReserveTableForm()

    context = {'form': reserve_form}

    return render(request, 'reserve_table.html', context)


class ReservationList(generic.ListView):
    model = Reservations
    queryset = Reservations.objects.all()
    template_name = 'reservation_list.html'
    paginate_by = 6


class ReservationDetail(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Reservations.objects.all()
        reservation = get_object_or_404(queryset, slug=slug)

        return render(
            request,
            'reservation_detail.html',
            {
                "reservation": reservation,
            }
            )
