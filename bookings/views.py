from django.shortcuts import render, get_object_or_404, HttpResponse
from django.views import generic, View
from django.views.generic.edit import DeleteView, UpdateView
from django.http import HttpResponseRedirect
from .models import Booking, OpeningHours
from .forms import BookTableForm
from .booking import confirm_availability, get_available_tables, get_opening_hours, generate_request_end
from datetime import datetime


def show_tables(request):
    current_date_str = str(datetime.now().date())
    current_date_weekday = datetime.strptime(str(current_date_str), '%Y-%m-%d').weekday()
    
    opens_closes = get_opening_hours(current_date_weekday)
    opening_time_str = str(opens_closes[0])[0:2]
    closing_time_str = str(opens_closes[1])[0:2]

    available_times = []

    for i in range(int(opening_time_str), int(closing_time_str)-2):
        time_to_test = ':00:00'
        number_guests = 12
        generate_request_start = current_date_str + ' ' + str(i) + time_to_test
        if confirm_availability(generate_request_start, number_guests):
            available_times.append(f'{i}:00 ')
        if i < int(closing_time_str)-3:
            for minute in range(15,60,15):
                time_to_add = str(minute)
                time_to_test = ':' + time_to_add + ':00'
                if confirm_availability(generate_request_start, number_guests):
                    available_times.append(f'{i}:{minute} ')
        
    return HttpResponse(available_times)


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
    fields = ['first_name', 'last_name', 'number_guests', 'comment']
    template_name_suffix = '_update_form'
    success_url = '/bookings/'
