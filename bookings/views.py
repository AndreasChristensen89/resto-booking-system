from django.shortcuts import render, get_object_or_404, HttpResponse
from django.views import generic, View
from django.views.generic.edit import DeleteView, UpdateView
from django.http import HttpResponseRedirect
from .models import Booking, Table
from restaurant.models import BookingDetails
from .forms import BookTableForm
from .booking import return_tables, double_booking, get_available_tables
import datetime


def book_table(request):
    form = BookTableForm()

    if request.method == 'POST':
        form = BookTableForm(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.author = request.user
            obj.save()
            # save the many-to-many data for the form.
            # overlapping_bookings = double_booking(obj.booking_start)
            tables = return_tables(obj.booking_start, obj.number_guests)
            auto_assign = BookingDetails.objects.all()[0].auto_table_assign
            if auto_assign and tables:
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
    request_start_str = '2021-11-06 17:00:00'
    request_end_str = '2021-11-06 20:00:00'
    request_start = datetime.datetime.strptime(request_start_str, '%Y-%m-%d %H:%M:%S')
    request_end = datetime.datetime.strptime(request_end_str, '%Y-%m-%d %H:%M:%S')
    
    double_booked = True
    # unavailable_tables = []
    
    # # 1. Remove existing reserv. that have the same start-time
    # tables_check_temp = Booking.objects.filter(
    #     # author=author,
    #     booking_start=request_start)
    # for table in tables_check_temp:
    #     unavailable_tables.append(table)
    # # 2. Remove existing reserv. that start before request-start but finish after
    # tables_check_temp_two = Booking.objects.filter(
    #     # author=author,
    #     booking_start__lt=request_start,
    #     booking_end__gt=request_start)
    # for table in tables_check_temp_two:
    #     unavailable_tables.append(table)
    # # 3. Remove existing reserv. that start before and finish after request-end
    # tables_check_temp_three = Booking.objects.filter(
    #     # author=author,
    #     booking_start__lt=request_end,
    #     booking_end__gt=request_end)
    # for table in tables_check_temp_three:
    #     unavailable_tables.append(table)
    
    # if unavailable_tables:
    #     double_booked = True

    bookings = Booking.objects.all()
    for booking in bookings:
        double_booked = False
        break

    return HttpResponse(double_booked)
