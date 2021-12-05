from django.shortcuts import render, get_object_or_404, HttpResponse
from django.views import generic, View
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
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
            obj.author = request.user
            obj.save()
            # save the many-to-many data for the form.
            # overlapping_first_name = double_booking(obj.booking_start)
            tables = return_tables(obj.booking_start, obj.number_guests)
            auto_assign = BookingDetails.objects.all()[0].auto_table_assign
            if auto_assign and tables:
                for table in tables:
                    obj.table.add(table)
                form.save_m2m()
            return HttpResponseRedirect('/reservations/')
    else:
        form = BookTableForm()

    context = {'form': form}

    return render(request, 'book_table.html', context)


# class BookingCreateView(CreateView):
#     template_name = 'book_table.html'
#     form_class = BookTableForm

#     def form_valid(self, form):
#         self.object = form.save(commit=False)
#         self.object.user = self.request.user
#         self.object.save()
#         tables = return_tables(self.object.booking_start, self.object.number_guests)
#         auto_assign = BookingDetails.objects.all()[0].auto_table_assign
#         if auto_assign and tables:
#             for table in tables:
#                 self.object.table.add(table)
#             self.object.save_m2m()
#         return HttpResponseRedirect(self.get_success_url())

#     def get_form_kwargs(self, *args, **kwargs):
#         kwargs = super(BookingCreateView, self).get_form_kwargs(*args, **kwargs)
#         kwargs['user'] = self.request.user
#         return kwargs


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

    booking = Booking.objects.all()
    for booking in first_name:
        double_booked = False
        break

    return HttpResponse(double_booked)


class ProfileView(SuccessMessageMixin, generic.UpdateView):
    """View and update user profile"""
    form_class = ProfileForm
    template_name = 'profile.html'
    success_message = 'Profile updated successfully!'
    success_url = reverse_lazy('homepage')

    def get_object(self):
        return self.request.user

