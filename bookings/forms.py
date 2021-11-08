from django import forms
from datetime import timedelta, datetime
from .models import Table, Booking, OpeningHours


class BookTableForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['first_name', 'last_name', 'number_guests', 'booking_start', 'table', 'comment']


class GuestRequestForm(forms.Form):
    date_and_time = forms.DateTimeField(label='Date and time')
    number_guests = forms.IntegerField(label='Guests')
