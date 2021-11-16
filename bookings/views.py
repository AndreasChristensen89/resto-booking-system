from django.shortcuts import render, get_object_or_404, HttpResponse
from django.views import generic, View
from django.views.generic.edit import DeleteView, UpdateView
from django.http import HttpResponseRedirect
from .models import Booking
from .forms import BookTableForm
from .booking import confirm_availability
from datetime import datetime


def show_tables(request):
    current_date = datetime.now().date()
    current_date_weekday = datetime.strptime(str(current_date), '%Y-%m-%d').weekday()

    all_bookings = Booking.objects.all()
    bookings_today = []
    for i in range(current_date_weekday, 7):
        for booking in all_bookings:
            date_of_booking = datetime.strptime(str(booking.booking_start), '%Y-%m-%d %H:%M:%S').date()
            if current_date == date_of_booking:
                bookings_today.append(booking.booking_start)

    return HttpResponse(current_date_weekday)


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
