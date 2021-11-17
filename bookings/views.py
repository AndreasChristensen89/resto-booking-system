from django.shortcuts import render, get_object_or_404, HttpResponse
from django.views import generic, View
from django.views.generic.edit import DeleteView, UpdateView
from django.http import HttpResponseRedirect
from .models import Booking, OpeningHours
from .forms import BookTableForm
from .booking import confirm_availability, get_available_tables
from datetime import datetime


def show_tables(request):
    current_date_str = str(datetime.now().date())
    current_date_weekday = datetime.strptime(str(current_date_str), '%Y-%m-%d').weekday()
    
    list_times = []
    opening_time = OpeningHours.objects.filter(
        weekday=current_date_weekday).values('from_time')
    closing_time = OpeningHours.objects.filter(
        weekday=current_date_weekday).values('to_time')
    for opening in opening_time:
        list_times.append(opening)
    for closing in closing_time:
        list_times.append(closing)
    extracted_times = []
    for time in range(len(list_times)):
        for key in list_times[time]:
            extracted_times.append(list_times[time][key])
    opening_time_str = str(extracted_times[0])[0:2]
    closing_time_str = str(extracted_times[1])[0:2]

    list_to_check_for_ok = []
    for i in range(int(opening_time_str), int(closing_time_str)-1):
        time_to_test = ':00:00'
        number_guests = 10
        generate_request_start = current_date_str + ' ' + str(i) + time_to_test
        available_tables_fullhour = get_available_tables(generate_request_start)
        time_to_test = ':30:00'
        available_tables_halfhour = get_available_tables(generate_request_start)
        sum_full = 0
        sum_half = 0
        for table in available_tables_fullhour:
            sum_full += table.size
        for table in available_tables_halfhour:
            sum_half += table.size
        if sum_full >= number_guests:
            list_to_check_for_ok.append(f'{i} is ok - ')
        if sum_half >= number_guests:
            list_to_check_for_ok.append(f'{i}:30 is ok - ')

    return HttpResponse(list_to_check_for_ok)


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
                    # Tables added after save since the object needs to exist before m2m comes in
                    obj.table.add(table)
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
    queryset = Booking.objects.all()
    context_object_name = "updated_list"
    template_name = 'updated_bookings.html'
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
    fields = ['first_name', 'last_name', 'comment']
    template_name_suffix = '_update_form'
    success_url = '/bookings/'
