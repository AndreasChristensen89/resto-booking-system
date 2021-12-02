from django import forms
from django.forms.widgets import SplitDateTimeWidget
from allauth.account.forms import SignupForm, LoginForm, ChangePasswordForm, ResetPasswordForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from .models import Booking
from restaurant.models import BookingDetails
import datetime
from .booking import return_tables, test_time, get_opening_hours


class BookTableForm(forms.ModelForm):
    booking_start = forms.SplitDateTimeField()
    
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
            raise forms.ValidationError(f'Not within opening hours: {opening_hours[0].from_time} to {opening_hours[0].to_time}')
        if not tables:
            raise forms.ValidationError("There are unfortunately not enough tables to accomodate your party")


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
