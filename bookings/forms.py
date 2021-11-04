from django import forms
from .models import Booking


class BookTableForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['first_name', 'last_name', 'email', 'phone', 'number_guests', 'date', 'booking_start', 'booking_end', 'comment']