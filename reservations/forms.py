from django import forms
from .models import Reservations


class ReserveTableForm(forms.ModelForm):
    class Meta:
        model = Reservations
        fields = ['first_name', 'last_name', 'email', 'phone', 'number_guests', 'date', 'time']
