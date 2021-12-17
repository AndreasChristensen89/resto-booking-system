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
from .booking import double_booking, return_tables
import datetime
from datetime import timedelta


def book_table(request):
    form = BookTableForm()

    if request.method == 'POST':
        form = BookTableForm(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            user = request.user
            obj.author = user
            booking_end = obj.booking_start + timedelta(minutes=BookingDetails.objects.all()[0].booking_duration)
            obj.booking_end = booking_end
            obj.save()
            # save the many-to-many data for the form.
            sorting_method = BookingDetails.objects.all()[0].table_assign_method
            tables = return_tables(obj.booking_start, obj.number_guests, sorting_method)
            limit = BookingDetails.objects.all()[0].assign_method_limit
            conflicting = double_booking(obj.booking_start, user)
            # conflicting length is 1 due to save further up
            if conflicting == 1 and sorting_method > 0 and tables and obj.number_guests < limit:
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

# currently not used
class BookingUpdated(generic.ListView):
    model = Booking
    context_object_name = "updated_list"
    queryset = Booking.objects.filter(
        status=1
    )
    template_name = 'updated_booking.html'

# currently not used
class BookingPending(generic.ListView):
    model = Booking
    context_object_name = "pending_list"
    queryset = Booking.objects.filter(
        status=0
    )
    template_name = 'booking_pending.html'

# currently not used
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

# tested
class CancelBookingView(DeleteView):
    model = Booking
    success_url = '/reservations/'

# tested
class UpdateReservationView(UpdateView):
    model = Booking
    fields = ['comment']
    template_name_suffix = '_update_form'
    success_url = '/reservations/'

# currently not used
class UpdateReservationViewAdmin(UpdateView):
    model = Booking
    fields = ['number_guests', 'table', 'comment', 'status']
    template_name_suffix = '_update_form_admin'
    success_url = '/reservations/updated_reservations/'

# currently not used
class ApproveReservationViewAdmin(UpdateView):
    model = Booking
    fields = ['table', 'status']
    template_name_suffix = '_approve_form'
    success_url = '/reservations/pending_booking/'


# tested
class ProfileView(SuccessMessageMixin, generic.UpdateView):
    """View and update user profile"""
    form_class = ProfileForm
    template_name = 'profile.html'
    success_message = 'Profile updated successfully!'
    success_url = reverse_lazy('homepage')

    def get_object(self):
        return self.request.user

