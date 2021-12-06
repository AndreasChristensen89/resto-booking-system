from django.shortcuts import render, get_object_or_404, HttpResponse
from django.views import generic, View
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from .models import Booking
from restaurant.models import BookingDetails
from .forms import BookTableForm, ProfileForm
from allauth.account.views import PasswordChangeView, PasswordResetView
from .booking import return_tables, double_booking
import datetime


def book_table(request):
    form = BookTableForm()

    if request.method == 'POST':
        form = BookTableForm(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            user = request.user
            obj.author = user
            obj.save()
            # save the many-to-many data for the form.
            tables = return_tables(obj.booking_start, obj.number_guests)
            auto_assign = BookingDetails.objects.all()[0].auto_table_assign
            conflicting = double_booking(obj.booking_start, user)
            # conflicting length is 1 due to save further up
            if conflicting == 1 and auto_assign and tables:
                for table in tables:
                    obj.table.add(table)
                form.save_m2m()
            return HttpResponseRedirect('/reservations/')
    else:
        form = BookTableForm()

    context = {'form': form}

    return render(request, 'book_table.html', context)


class BookingList(generic.ListView):
    model = Booking
    queryset = Booking.objects.all()
    template_name = 'booking_list.html'
    paginate_by = 6


class BookingUpdated(generic.ListView):
    model = Booking
    context_object_name = "updated_list"
    queryset = Booking.objects.filter(
        status=1
    )
    template_name = 'updated_booking.html'


class BookingPending(generic.ListView):
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
    success_url = '/reservations/'


class UpdateReservationView(UpdateView):
    model = Booking
    fields = ['comment']
    template_name_suffix = '_update_form'
    success_url = '/reservations/'


class UpdateReservationViewAdmin(UpdateView):
    model = Booking
    fields = ['number_guests', 'table', 'comment', 'status']
    template_name_suffix = '_update_form_admin'
    success_url = '/reservations/updated_reservations/'


class ApproveReservationViewAdmin(UpdateView):
    model = Booking
    fields = ['table', 'status']
    template_name_suffix = '_approve_form'
    success_url = '/reservations/pending_booking/'


def show_tables(request):
    # User = get_user_model()
    # users = User.objects.all()
    # list_of_user_ids = []
    # for user in users:
    #     list_of_user_ids.append(user.id)
    #     list_of_user_ids.append(" ")

    request_start_str = '2021-10-06 18:00:00'
    request_end_str = '2021-11-06 15:00:00'
    request_start = datetime.datetime.strptime(request_start_str, '%Y-%m-%d %H:%M:%S')
    request_end = datetime.datetime.strptime(request_end_str, '%Y-%m-%d %H:%M:%S')

    # double_booked = True
    # bookings = Booking.objects.all()
    # list_of_bookings_authors_ids = []
    # for booking in bookings:
    #     if str(booking.booking_start) == request_start_str:
    #         list_of_bookings_authors_ids.append(booking.author.id)
    #         double_booked = False

    conflicting = double_booking(request_start_str)

    return HttpResponse(conflicting)


class ProfileView(SuccessMessageMixin, generic.UpdateView):
    """View and update user profile"""
    form_class = ProfileForm
    template_name = 'profile.html'
    success_message = 'Profile updated successfully!'
    success_url = reverse_lazy('homepage')

    def get_object(self):
        return self.request.user

