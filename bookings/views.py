from django.shortcuts import render, get_object_or_404, HttpResponse
from django.views import generic, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.http import HttpResponseRedirect
from .models import Booking, Table
from .forms import BookTableForm
from .booking import confirm_availability


def book_table(request):
    book_form = BookTableForm()

    if request.method == 'POST':
        book_form = BookTableForm(request.POST)
        table = confirm_availability("2021-11-06 17:00", 4)

        if book_form.is_valid():
            obj = book_form.save(commit=False)
            obj.author = request.user
            obj.save()
            return HttpResponseRedirect('/bookings/')
            obt.table.add(table)
            obj.save()
            for table in table:
                if table.size == 4:
                    print(table)
    else:
        book_form = BookTableForm()

    context = {'form': book_form}

    return render(request, 'book_table.html', context)


def show_tables(request):
    request_end = "2021-11-06 20:00"
    
    unavailable_tables = []

    # Exclude tables that have the same start time
    tables_check_temp = Booking.objects.filter(
        booking_start="2021-11-06 17:00").values('table')    # returns {'table': 7}
    for table in tables_check_temp:
        unavailable_tables.append(table)
    
    # Exclude tables that start before requested start + end after requested start
    tables_check_temp = Booking.objects.filter(
        booking_start__lt="2021-11-06 17:00",
        booking_end__gt="2021-11-06 17:00").values('table')
    for table in tables_check_temp:
        unavailable_tables.append(table)
    
    # Exclude tables that start before end of request + end after end of request
    tables_check_temp = Booking.objects.filter(
        booking_start__lt=request_end,
        booking_end__gt=request_end).values('table')
    for table in tables_check_temp:
        unavailable_tables.append(table)

    # Take all tables and remove the ones from unavailable_tables
    tables = Table.objects.all()
    for table in tables:
        if table in unavailable_tables:
            tables.remove(table)

    return HttpResponse(unavailable_tables)


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
