from django.shortcuts import render, get_object_or_404, HttpResponse
from django.views import generic, View
from django.views.generic.edit import DeleteView, UpdateView
from django.http import HttpResponseRedirect
from .models import Booking, BookingDetails, Table
from .forms import BookTableForm
from .booking import return_tables, get_available_tables, get_opening_hours, test_available_times, number_of_guests
from datetime import datetime, timedelta


def book_table(request):
    book_form = BookTableForm()

    if request.method == 'POST':
        book_form = BookTableForm(request.POST)

        if book_form.is_valid():
            obj = book_form.save(commit=False)
            obj.author = request.user
            tables = return_tables(str(obj.booking_start), obj.number_guests)
            if len(tables) < 1:
                raise Exception("There are unfortunately not enough tables to accomodate your party")
            obj.save()

            if tables is not None:
                for table in tables:
                    obj.table.add(table)
            obj.save()
            return HttpResponseRedirect('/bookings/')
    else:
        book_form = BookTableForm()
    
    context = {'form': book_form}

    return render(request, 'book_table.html', context)


class BookingList(generic.ListView):
    model = Booking
    queryset = Booking.objects.all()
    template_name = 'booking_list.html'
    paginate_by = 6


class BookingsUpdated(generic.ListView):
    model = Booking
    context_object_name = "updated_list"
    queryset = Booking.objects.filter(
        status=1
    )
    template_name = 'updated_bookings.html'


class BookingsPending(generic.ListView):
    model = Booking
    context_object_name = "pending_list"
    queryset = Booking.objects.filter(
        status=0
    )
    template_name = 'booking_pending.html'


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
    fields = ['comment']
    template_name_suffix = '_update_form'
    success_url = '/bookings/'


class UpdateReservationViewAdmin(UpdateView):
    model = Booking
    fields = ['number_guests', 'table', 'comment', 'status']
    template_name_suffix = '_update_form_admin'
    success_url = '/bookings/updated_reservations/'


class ApproveReservationViewAdmin(UpdateView):
    model = Booking
    fields = ['table', 'status']
    template_name_suffix = '_approve_form'
    success_url = '/bookings/pending_bookings/'


def show_tables(request):
    request_start = '2021-11-06 17:00:00'
    number_guests = 24
    available_tables = get_available_tables(request_start)

    # Sort list from higest to lowest
    available_tables.sort(key=lambda x: x.size, reverse=True)
    tables_sorted = sorted(available_tables, key=lambda x: x.size, reverse=True)

    table_combination = []
    sum = 0
    for table in tables_sorted:
        if sum < number_guests:
            table_combination.append(table)
            sum += table.size
        # elif sum > number_guests:
        #     combination = table_combination
        #     combination.pop()
        #     if sum - table.size == number_guests
    return HttpResponse(table_combination)
