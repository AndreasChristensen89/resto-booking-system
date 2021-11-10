from django import forms
from .models import Booking
from django.contrib.admin import widgets


class BookTableForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            'first_name', 'last_name', 'number_guests', 'booking_start', 'table', 'comment'
            ]
