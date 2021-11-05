from datetime import timedelta
from .models import Table, Booking, OpeningHours


def book_restaurant_table(booking_start, number_guests, minutes_slot=90):
    """
    This method uses get_first_table_available to get the first table available, then it
    creates a Booking on the database.
    """
    table = get_table_available(booking_start, number_guests, minutes_slot)

    if table:
        delta = timedelta(seconds=60*minutes_slot)
        booking = Booking(table=table)
        booking.save()
        return {'booking': booking.slug, 'table': table.id}
    else:
        return None

def get_table_available(booking_start, number_guests, minutes_slot=180):
    """
    This method returns the first available table of a restaurant, given a specific number of
    people and a booking date/time.
    """
    delta = timedelta(seconds=60*minutes_slot)
    request_start = booking_start
    request_end = booking_start + delta

    all_tables = Table.objects.all()
    tables_booked = []

    # Exclude tables which start and end booking date includes requested initial booking date_time
    tables_check = Booking.objects.filter(
        booking_start=request_start,
        booking_end=request_start).values('table')
    for x in tables_check:
        tables_booked.append(x)
    
    tables_check_two = Booking.objects.filter(
        booking.start > request_end,
        booking.end < request_start).values('table')
    for x in tables_check_two:
        tables_booked.append(x)
    
    tables_check_three = Booking.objects.filter(
        booking.start > request_end,
        booking.end < request_start).values('table')
    for x in tables_check_three:
        tables_booked.append(x)
