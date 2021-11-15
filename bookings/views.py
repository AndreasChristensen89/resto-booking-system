from django.shortcuts import render, get_object_or_404, HttpResponse
from django.views import generic, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.http import HttpResponseRedirect
from .models import Booking, Table
from .forms import BookTableForm
from .booking import get_available_tables, confirm_availability
from datetime import timedelta


def book_table(request):
    book_form = BookTableForm()

    if request.method == 'POST':
        book_form = BookTableForm(request.POST)
        request_start = book_form.data['booking_start']
        number_guests = book_form.data['number_guests']
        tables = confirm_availability(request_start, number_guests)

        if book_form.is_valid():
            obj = book_form.save(commit=False)
            obj.author = request.user
            obj.save()
            if tables is not None:
                for table in tables:
                    obj.table.add(table)   # Tables added after save since the object needs to exist before m2m comes in
            return HttpResponseRedirect('/bookings/')
    else:
        book_form = BookTableForm()

    context = {'form': book_form}

    return render(request, 'book_table.html', context)


def show_tables(request):
    available_tables = get_available_tables("2021-11-07 17:00", 9)
    number_guests = 17
    fitting_tables = []
    
    spots_to_fill = number_guests

    table_id = 0
    
    for table in available_tables:
        if table.size == int(number_guests):
            fitting_tables.append(table)
            spots_to_fill = 0
            table_id = table.id
            break
    if spots_to_fill == number_guests:
        for table in available_tables:
            if table.size-1 == int(number_guests):
                fitting_tables.append(table)
                spots_to_fill = 0
                table_id = table.id
                break
    # high number to be sure that new combination is lower
    best_combination = 100
    # how many seats gained/wasted. > 0 = wasted
    seat_difference = 0
    if spots_to_fill == int(number_guests):
        for i in range(0, len(available_tables)-1):
            for j in range(i+1, len(available_tables)):
                combination = available_tables[i].size + available_tables[j].size
                seat_difference = int(number_guests)-combination
                if seat_difference <= 0 and abs(seat_difference) < abs(best_combination):
                    best_combination = seat_difference
                    fitting_tables = []
                    fitting_tables.append(available_tables[i])
                    fitting_tables.append(available_tables[j])

    return HttpResponse(fitting_tables)


class BookingList(generic.ListView):
    model = Booking
    queryset = Booking.objects.all()
    template_name = 'booking_list.html'
    paginate_by = 6


class BookingDetail(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Booking.objects.all()
        booking = get_object_or_404(queryset, slug=slug)

        return render(
            request,
            'booking_detail.html',
            {
                "booking": booking,
            }
            )


class CancelBookingView(DeleteView):
    model = Booking
    success_url = '/bookings/'


class UpdateReservationView(UpdateView):
    model = Booking
    fields = ['first_name', 'last_name', 'number_guests', 'booking_start', 'comment']
    template_name_suffix = '_update_form'
    success_url = '/bookings/'
