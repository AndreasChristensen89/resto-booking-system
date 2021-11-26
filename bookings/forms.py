from django import forms
from .models import Booking
import datetime
from .booking import return_tables, test_time, get_opening_hours


class BookTableForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            'first_name', 'last_name', 'number_guests', 'booking_start', 'comment'
            ]
    
    def clean(self):
        number_guests = self.cleaned_data.get('number_guests')
        booking_start = self.cleaned_data.get('booking_start')
        author = self.cleaned_data.get('author')

        tables = return_tables(booking_start, number_guests)

        if not test_time(booking_start):
            opening_hours = get_opening_hours(booking_start.weekday())
            raise forms.ValidationError(f'Not within opening hours: {opening_hours[0].from_time} to {opening_hours[0].to_time}')
        if not tables:
            raise forms.ValidationError("There are unfortunately not enough tables to accomodate your party")
        # Check for similar author and similar names
        bookings_author = Booking.objects.filter(
            author=author, booking_start=booking_start
        )
        if bookings_author:
            raise forms.ValidationError("Booking already exists for this date and time")


class DateAndGuestsForm(forms.Form):
    day = forms.DateField(initial=datetime.date.today)
    number = forms.IntegerField()
