from django import forms
from django.forms.widgets import SplitDateTimeWidget
from allauth.account.forms import SignupForm, LoginForm, ChangePasswordForm, ResetPasswordForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from .models import Booking
from restaurant.models import BookingDetails
import datetime
from .booking import return_tables, test_time, get_opening_hours, double_booking


class BookTableForm(forms.ModelForm):
    booking_start = forms.SplitDateTimeField()
    
    # def __init__(self, *args, **kwargs):
    #     self.user = kwargs.pop('user', None)
    #     super(BookTableForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Booking
        fields = [
            'first_name', 'last_name', 'number_guests', 'booking_start', 'comment'
            ]

    def clean(self):
        number_guests = self.cleaned_data.get('number_guests')
        booking_start = self.cleaned_data.get('booking_start')

        tables = return_tables(booking_start, number_guests)
        

        if not test_time(booking_start):
            opening_hours = get_opening_hours(booking_start.weekday())
            open = str(opening_hours[0].from_time)[0:5]
            close = str(opening_hours[0].to_time)[0:5]
            raise forms.ValidationError(f'Not within opening hours of the requested date - {open} to {close}')
        if not tables:
            raise forms.ValidationError("There are unfortunately not enough tables to accomodate your party")
        # if Booking.objects.filter(booking_author=user).exists():
        #     raise forms.ValidationError("You have already booked a time on the requested time")


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
