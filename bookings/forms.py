from django import forms
from .models import Booking
import datetime
from .booking import return_tables, test_time


class BookTableForm(forms.ModelForm):
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
            raise forms.ValidationError("Not within opening hours")
        if not tables:
            raise forms.ValidationError("There are unfortunately not enough seats to accomodate your party at the requested time")


class DateAndGuestsForm(forms.Form):
    day = forms.DateField(initial=datetime.date.today)
    number = forms.IntegerField()
