from django.shortcuts import render, get_object_or_404, HttpResponse
from django.views import generic, View
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from .models import Booking
from restaurant.models import BookingDetails, OpeningHours
from .forms import BookTableForm, ProfileForm
from allauth.account.views import PasswordChangeView, PasswordResetView
from .booking import double_booking, return_tables, return_all_available_tables
import datetime
from datetime import timedelta


def book_table(request):
    """
    View for booking table. Attaches the user logged in, adds the end-time of the booking
    ManytoManyfield (tables) must be added after object exists, so double-save
    Checks sorting method and fetches tables, checks nbr of tables and limit for sorting
    If user has conflicting booking it sends an email and assigns no tables
    """
    form = BookTableForm()
    opening_list = OpeningHours.objects.all()

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
            elif conflicting > 1:
                subject = "Dre's Diner booking"
                body = (
                    f"Hello {user.first_name}. " +
                    f"It appears that you have made two overlapping reservations. "
                    f"Your new reservation on the {obj.booking_start} has therefore not been assigned any tables, it is however still kept on your page. " +
                    "Please contact us if this is intentional, otherwise you can safely delete the new reservation. " +
                    "We look forward to having you."
                )
                # Send Confirmation Mail to user and CC to admin
                send_mail(
                    subject,
                    body,
                    'dresdiner@email.com',
                    [user.email, 'dresdiner@email.com']
                )
            return HttpResponseRedirect('/reservations/bookings/')
    else:
        form = BookTableForm()

    context = {'form': form, 'opening_list': opening_list}

    return render(request, 'book_table.html', context)


class BookingList(generic.ListView):
    """
    Gets the user logged in and uses it in filter
    Template sorts for bookings in future
    """
    model = Booking

    def get_queryset(self):
        current_datetime = datetime.datetime.now()
        queryset = super(BookingList, self).get_queryset()
        queryset = queryset.filter(
            author=self.request.user,
            booking_start__gt=current_datetime)
        return queryset
    template_name = 'booking_list.html'
    paginate_by = 3


class BookingListPrevious(generic.ListView):
    """
    Gets the user logged in and uses it in filter
    Template sorts for bookings in past
    """
    model = Booking

    def get_queryset(self):
        current_datetime = datetime.datetime.now()
        queryset = super(BookingListPrevious, self).get_queryset()
        queryset = queryset.filter(
            author=self.request.user,
            booking_start__lt=current_datetime)
        return queryset
    template_name = 'booking_list_previous.html'
    paginate_by = 3


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


class BookingDetailPrevious(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Booking.objects.all()
        booking = get_object_or_404(queryset, slug=slug)

        return render(
            request,
            'booking_detail_previous.html',
            {
                "booking": booking,
            }
            )


class BookingUpdated(generic.ListView):
    """
    Gets all non-declined booking with comments
    Template sorts for updates
    """
    model = Booking
    context_object_name = "updated_list"
    queryset = Booking.objects.exclude(comment__exact='').exclude(status=2)
    template_name = 'updated_booking.html'
    paginate_by = 6


class BookingPending(generic.ListView):
    """
    Gets all pending bookings
    """
    model = Booking
    context_object_name = "pending_list"
    queryset = Booking.objects.filter(
        status=0
    )
    template_name = 'pending_bookings.html'
    paginate_by = 3


class CancelBookingView(DeleteView):
    """
    User and admin can cancel a booking
    """
    model = Booking
    success_url = '/reservations/bookings/'


class UpdateReservationView(UpdateView):
    """
    User can update comment here
    """
    model = Booking
    fields = ['comment']
    template_name_suffix = '_update_form'
    success_url = '/reservations/bookings/'


class UpdateReservationViewAdmin(UpdateView):
    """
    Admin can update booking details
    Meant for bookings that have new requests
    """
    model = Booking
    fields = ['number_guests', 'table', 'comment', 'status']
    template_name_suffix = '_update_form_admin'
    success_url = '/reservations/updated/'


class ApproveReservationViewAdmin(UpdateView):
    """
    Admin can update booking details here
    Meant for accepting/declining directly
    Sends emails to confirm action
    """
    model = Booking
    fields = ['table', 'status', 'comment']
    template_name_suffix = '_approve_form'
    success_url = '/reservations/pending/'

    def form_valid(self, form):
        subject = "Dre's Diner booking"
        body = ""
        status = form.cleaned_data.get('status')
        if status == 2:
            body = (
                f"Hello {self.object.author.first_name}. " +
                f"Unfortunately, we are not able to accomodate your booking on {self.object.booking_start}. " +
                f"For more information please see the comment left by the restaurant or contact us via our website."
            )
        elif status == 1:
            body = (
                f"Hello {self.object.author.first_name}, " +
                f"your booking is confirmed on {self.object.booking_start}. " +
                "Please note that cancellations must be made minimum two hours before. We look forward to seeing you."
            )
        if status != 0:
            send_mail(
                subject,
                body,
                'dresdiner@email.com',
                [self.object.author.email, 'dresdiner@email.com']
            )
        return super(ApproveReservationViewAdmin, self).form_valid(form)

class AvailableTables(View):
    def get(self, request, slug, *args, **kwargs):
        queryset = Booking.objects.all()
        booking = get_object_or_404(queryset, slug=slug)
        list = return_all_available_tables(booking.booking_start, booking.booking_end)

        return render(
            request,
            'available_tables.html',
            {
                "list": list,
                "booking": booking,
            }
            )


class ProfileView(SuccessMessageMixin, generic.UpdateView):
    """
    View and update user profile
    """
    form_class = ProfileForm
    template_name = 'profile.html'
    success_message = 'Profile updated successfully!'
    success_url = reverse_lazy('homepage')

    def get_object(self):
        return self.request.user


def error_404(request, exception):
    data = {}
    return render(request, '404.html', data)


def error_500(request):
    data = {}
    return render(request, '500.html', data)
