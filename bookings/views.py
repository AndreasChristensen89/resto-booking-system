from django.shortcuts import render, get_object_or_404, HttpResponse
from django.template import loader
from django.views import generic, View
from django.views.generic.edit import DeleteView, UpdateView
from django.http import HttpResponseRedirect
from .models import Booking, OpeningHours
from .forms import BookTableForm, DateAndGuestsForm
from .booking import return_tables, get_available_tables, get_opening_hours, generate_request_end, display_available_times
from datetime import datetime


def times_available(request):
    list = display_available_times()
    template = loader.get_template('booking_test.html')
    return render(request, 'booking_test.html', {'available_times_list': list})


def get_date_and_guests(request):
    if request.method == 'POST':
        form = DateAndGuestsForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/firstform')
    else:
        form = DateAndGuestsForm()

    return render(request, 'select_date_form.html', {'form': form})


def show_tables(request):
    date = '2021-11-19 17:00:00'
    number_guests = 40
    date_weekday = datetime.strptime(date, '%Y-%m-%d %H:%M:%S').weekday()
    current_date = str(datetime.now().date())

    opens_closes = get_opening_hours(datetime.now().weekday())
    opening_time_str = str(opens_closes[0])[0:2]
    closing_time_str = str(opens_closes[1])[0:2]

    booking_interval = 30
    available_times = []

    for i in range(int(opening_time_str), int(closing_time_str)-2):
        time_to_test = ':00:00'
        start_to_pass = current_date + ' ' + str(i) + time_to_test
        available_tables = get_available_tables(start_to_pass)
        sum = 0
        for table in available_tables:
            sum += table.size
        if sum >= number_guests:
            available_times.append(f'{i}:00 ')
        if i < int(closing_time_str)-3:
            for minute in range(booking_interval, 60, booking_interval):
                time_to_add = str(minute)
                time_to_test = ':' + time_to_add + ':00'
                available_tables = get_available_tables(start_to_pass)
                sum = 0
                for table in available_tables:
                    sum += table.size
                if sum >= number_guests:
                    available_times.append(f'{i}:{minute} ')

    return HttpResponse(date_weekday)


def book_table(request):
    to_add = '2021-11-29 17:00:00'
    book_form = BookTableForm()

    if request.method == 'POST':
        book_form = BookTableForm(request.POST)

        if book_form.is_valid():
            obj = book_form.save(commit=False)
            obj.author = request.user
            obj.booking_start = datetime.strptime(to_add, '%Y-%m-%d %H:%M:%S')
            obj.save()

            request_start = str(obj.booking_start)
            number_guests = book_form.data['number_guests']
            tables = return_tables(request_start, number_guests)

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
    fields = ['number_guests', 'table', 'comment']
    template_name_suffix = '_update_form_admin'
    success_url = '/bookings/updated_reservations/'
