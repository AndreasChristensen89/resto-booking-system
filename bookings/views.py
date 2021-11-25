from django.shortcuts import render, get_object_or_404, HttpResponse
from django.views import generic, View
from django.views.generic.edit import DeleteView, UpdateView
from django.http import HttpResponseRedirect
from .models import Booking
from .forms import BookTableForm
from .booking import return_tables, get_available_tables, get_opening_hours, display_available_times
from datetime import datetime


def book_table(request):
    book_form = BookTableForm()
    # number = request.POST.get('number')     # 12
    # date = request.POST.get('day')  # 2021-12-25
    # list = display_available_times(request.POST.get('date'), request.POST.get('number_guests'))

    if request.method == 'POST':
        book_form = BookTableForm(request.POST)

        if book_form.is_valid():
            obj = book_form.save(commit=False)
            # datetime_str = str(date) + ' ' + '15:00'
            # datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
            # obj.number_guests = number
            obj.author = request.user
            # obj.booking_start = datetime_to_add
            # obj.booking_start = datetime.strptime(datetime_to_add, '%Y-%m-%d %H:%M')
            tables = return_tables(str(obj.booking_start), obj.number_guests)
            if len(tables) < 1:
                raise Exception("No tables were found")
            obj.save()

            if tables is not None:
                for table in tables:
                    obj.table.add(table)
            obj.save()
            return HttpResponseRedirect('/bookings/')
    else:
        book_form = BookTableForm()
    
    context = {'form': book_form}
    # context = {'form': book_form, 'available_times_list': list, 'number': number, 'date': date}

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
