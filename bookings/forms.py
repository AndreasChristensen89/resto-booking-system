from django import forms
from datetime import timedelta, datetime
from .models import Table, Booking, OpeningHours


class CheckTableForm(forms.ModelForm):
    class Meta:
        fields = ['number_guests', 'booking_start']


class BookTableForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['first_name', 'last_name', 'number_guests', 'booking_start', 'table', 'comment']


# def book_restaurant_table(booking_start, number_guests, minutes_slot=180):
#     """
#     This method uses get_table_available to get the first table available, then it
#     creates a Booking on the database.
#     """
#     table = get_available_tables(booking_start, number_guests, minutes_slot)

#     if table:
#         # delta = timedelta(seconds=60*minutes_slot)
#         booking = Booking(table=table)
#         booking.save()
#         return {'booking': booking.slug, 'table': table.id}
#     else:
#         return None


def get_available_tables(request_start, number_guests, minutes_slot=180):
    """
    This method returns the first available table of a restaurant, given a specific number of
    people and a booking date/time.
    """
    delta = timedelta(seconds=60*minutes_slot)
    request_end = request_start + delta
    
    tables_unavailable = []

    # Exclude tables that have the same start time
    tables_check_temp = Booking.objects.filter(
        booking_start=request_start).values('table')
    for table in tables_check_temp:
        tables_unavailable.append(table)
    
    # Exclude tables that start before requested start + end after requested start
    tables_check_temp = Booking.objects.filter(
        booking_start__lt=request_start,
        booking_end__gt=request_start).values('table')
    for table in tables_check_temp:
        tables_unavailable.append(table)
    
    # Exclude tables that start before end of request + end after end of request
    tables_check_temp = Booking.objects.filter(
        booking_start__lt=request_end,
        booking_end__gt=request_end).values('table')
    for table in tables_check_temp:
        tables_unavailable.append(table)

    # Take all tables and remove the ones from unavailable_tables
    tables = Table.objects.all()
    for table in tables:
        if table in tables_unavailable:
            tables.remove(table)
    
    return tables


def confirm_availability(request_start, number_guests, minutes_slot=180):
    available_tables = get_available_tables(request_start, number_guests, minutes_slot=180)
    sum = 0

    for table in available_tables:
        sum += table.size
    
    if sum < number_guests:
        return False
    else:
        return True

# How to get weekday
# date_str='10-12-20'
# datetime_object = datetime.strptime(date_str, '%m-%d-%y')
# datetime_object.weekday()