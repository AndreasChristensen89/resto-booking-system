from django import forms
from .models import Booking
import datetime


class BookTableForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            'first_name', 'last_name', 'number_guests', 'booking_start', 'comment'
            ]


class DateAndGuestsForm(forms.Form):
    day = forms.DateField(initial=datetime.date.today)
    number = forms.IntegerField()
