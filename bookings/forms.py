from django import forms
from .models import Booking
import datetime


class BookTableForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            'first_name', 'last_name', 'comment'
            ]


class DateAndGuestsForm(forms.Form):
    day = forms.DateField(initial=datetime.date.today)
    number_guests = forms.IntegerField()


# class TimeForm(forms.Form):
