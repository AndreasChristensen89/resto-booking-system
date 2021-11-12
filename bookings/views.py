from django.shortcuts import render, get_object_or_404, HttpResponse
from django.views import generic, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.http import HttpResponseRedirect
from .models import Booking, Table
from .forms import BookTableForm
from .booking import get_available_tables


def book_table(request):
    book_form = BookTableForm()

    if request.method == 'POST':
        book_form = BookTableForm(request.POST)
        table = get_available_tables()

        if book_form.is_valid():
            obj = book_form.save(commit=False)
            obj.author = request.user
            obj.save()
            obj.table.set(table)
            obj.save()
            return HttpResponseRedirect('/bookings/')
    else:
        book_form = BookTableForm()

    context = {'form': book_form}

    return render(request, 'book_table.html', context)


def show_tables(request):
    # Test variable to simulate a date entered
    request_end = "2021-11-06 20:00"
    
    # List of all unavailable tables
    unavailable_tables = []

    # First remove tables that have the same start-time
    tables_check_temp = Booking.objects.filter(
        booking_start="2021-11-06 17:00").values('table')
    for table in tables_check_temp:
        unavailable_tables.append(table)
    
    # Second remove tables that start before but finish after start-time
    tables_check_temp = Booking.objects.filter(
        booking_start__lt="2021-11-06 17:00",
        booking_end__gt="2021-11-06 17:00").values('table')
    for table in tables_check_temp:
        unavailable_tables.append(table)
    
    # Third remove tables that that before end-time but finish after end-time
    tables_check_temp = Booking.objects.filter(
        booking_start__lt=request_end,
        booking_end__gt=request_end).values('table')
    for table in tables_check_temp:
        unavailable_tables.append(table)

    # Create a list of unavailable tables' ids
    list_unav = []
    for table in range(len(unavailable_tables)):
        for key in unavailable_tables[table]:
            list_unav.append(unavailable_tables[table][key])
    
    # Take all tables and sort out the ids from the unavailable list
    available_tables = []
    all_tables = Table.objects.all()
    for table in all_tables:
        if table.id not in list_unav:
            available_tables.append(table.id)
    
    table_to_return = Table.objects.get(id=available_tables[0])

    return HttpResponse(table_to_return)


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
