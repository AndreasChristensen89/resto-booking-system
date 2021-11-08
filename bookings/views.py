from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from django.views.generic.edit import DeleteView, UpdateView
from django.http import HttpResponseRedirect
from .models import Booking, Table
from .forms import BookTableForm, GuestRequestForm
from .booking import confirm_availability


class CheckAvailability(generic.ListView):
    model = Booking
    queryset = Booking.objects.all()
    template_name = 'check_availability.html'


def get_request(request):
    if request.method == 'POST':
        form = GuestRequestForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/bookings/book_table/')
    else:
        form = GuestRequestForm()
    
    return render(request, 'check_availability.html', {'form': form})


def book_table(request):
    book_form = BookTableForm()

    if request.method == 'POST':
        book_form = BookTableForm(request.POST)
        check_form_data = CheckTableForm.cleaned_data
        date_and_time = check_form_data['booking_start']
        nbr_guests = check_form_data['number_guests']

        if book_form.is_valid():
            obj = book_form.save(commit=False)
            obj.author = request.user
            obj.booking_start = date_and_time
            obj.number_guests = nbr_guests
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
    fields = ['first_name', 'last_name', 'number_guests', 'booking_start', 'table', 'comment']
    template_name_suffix = '_update_form'
    success_url = '/bookings/'
