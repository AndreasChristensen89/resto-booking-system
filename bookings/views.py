from django.shortcuts import render, get_object_or_404, HttpResponse
from django.views import generic, View
from django.views.generic.edit import DeleteView, UpdateView
from django.http import HttpResponseRedirect
from .models import Booking
from restaurant.models import BookingDetails
from .forms import BookTableForm
from .booking import return_tables, double_booking, get_unavailable_tables
from datetime import datetime


def book_table(request):
    form = BookTableForm()

    if request.method == 'POST':
        form = BookTableForm(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.author = request.user
            obj.save()
            # save the many-to-many data for the form.
            overlapping_times = get_unavailable_tables(request_start)
            if overlapping_times is None:
                tables = return_tables(obj.booking_start, obj.number_guests)
                auto_assign = BookingDetails.objects.all()[0].auto_table_assign
                if auto_assign and tables is not None:
                    for table in tables:
                        obj.table.add(table)
                    form.save_m2m()
            return HttpResponseRedirect('/bookings/')
    else:
        form = BookTableForm()

    context = {'form': form}

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
    author = 1
    request_start = '2022-01-07 10:00:00'
    request_end = '2022-01-07 13:00:00'
    double_booked = False
    
    bookings_exact = Booking.objects.filter(
        booking_start=request_start
    )
    bookings_before = Booking.objects.filter(
        author=author,
        booking_start__lt=request_start,
        booking_end__gt=request_start
    )
    bookings_after = Booking.objects.filter(
        author=author,
        booking_start__lt=request_end,
        booking_end__gt=request_end
    )

    if bookings_exact or bookings_before or bookings_after:
        double_booked = True

    return HttpResponse(double_booked)
