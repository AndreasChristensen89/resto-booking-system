from django import forms
from django.forms.widgets import SplitDateTimeWidget
from allauth.account.forms import SignupForm, LoginForm, ChangePasswordForm, ResetPasswordForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Booking
from restaurant.models import BookingDetails
from datetime import datetime, timedelta
from datetime import datetime
from .booking import return_tables, test_time, get_opening_hours, double_booking


class BookTableForm(forms.ModelForm):
    number_guests = forms.IntegerField(label='Number of guests')
    booking_start = forms.DateTimeField(label='Date and time', input_formats=['Y%/%m/%d %H:%M'])

    class Meta:
        model = Booking
        fields = [
            'number_guests', 'booking_start', 'comment'
            ]

    def clean(self):
        number_guests = self.cleaned_data.get('number_guests')
        booking_start = self.cleaned_data.get('booking_start')
        available_tables = []
        sorting_method = BookingDetails.objects.all()[0].table_assign_method
        if booking_start is not None:
            available_tables = return_tables(booking_start, number_guests, sorting_method)
            time_check = test_time(booking_start)

            if not time_check:
                opening_hours = get_opening_hours(booking_start.weekday())
                closing_hour_str = '01/01/01 ' + str(opening_hours[0].to_time)
                closing_hour_dt = datetime.strptime(closing_hour_str, '%d/%m/%y %H:%M:%S')

                booking_duration = BookingDetails.objects.all()[0].booking_duration
                latest_reservation = closing_hour_dt - timedelta(minutes=booking_duration)
                
                open = str(opening_hours[0].from_time)[0:5]
                close = str(latest_reservation)[11:16]
                raise forms.ValidationError(f'Reservations on the requested date can be made between {open} and {close}')
        if not available_tables and sorting_method > 0:
            raise forms.ValidationError("There are unfortunately not enough tables to accomodate your party at this time")
        if number_guests < 1:
            raise forms.ValidationError("Number of guests must be at least 1")
    
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.form_method = 'post'
    #     self.helper.add_input(Submit('submit', 'Save booking'))
        


class ProfileForm(UserChangeForm):
    """View and edit profile"""
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        """Meta class"""
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            )
