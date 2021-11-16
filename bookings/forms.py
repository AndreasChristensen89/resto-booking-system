from django import forms
from .models import Booking
from bootstrap_datepicker_plus import DatePickerInput


class BookTableForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            'first_name', 'last_name', 'number_guests', 'booking_start', 'comment'
            ]
        widgets = {
            'booking_starte': DatePickerInput(format='%d-%m-%Y'),
        }
