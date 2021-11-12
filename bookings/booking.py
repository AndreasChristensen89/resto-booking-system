from datetime import datetime, timedelta
from .models import Booking, Table


def get_available_tables():    # add request_start as parameter later
    """
    This method returns the first available table of a restaurant, given a specific number of
    people and a booking date/time.
    """
    # Test variable to simulate a date entered
    request_start = "2021-11-06 12:00"
    request_end = "2021-11-06 15:00"
    
    # List of all unavailable tables
    unavailable_tables = []

    # First remove tables that have the same start-time
    tables_check_temp = Booking.objects.filter(
        booking_start=request_start).values('table')
    for table in tables_check_temp:
        unavailable_tables.append(table)
    
    # Second remove tables that start before but finish after start-time
    tables_check_temp_two = Booking.objects.filter(
        booking_start__lt=request_start,
        booking_end__gt=request_start).values('table')
    for table in tables_check_temp_two:
        unavailable_tables.append(table)
    
    # Third remove tables that that before end-time but finish after end-time
    tables_check_temp_three = Booking.objects.filter(
        booking_start__lt=request_end,
        booking_end__gt=request_end).values('table')
    for table in tables_check_temp_three:
        unavailable_tables.append(table)

    # Create a list of unavailable tables' ids
    list_unav = []
    for table in range(len(unavailable_tables)):
        for key in unavailable_tables[table]:
            list_unav.append(unavailable_tables[table][key])
    
    # Take all tables and sort out the ids from the unavailable list
    available_tables = []
    all_tables = Table.objects.all()
    for table in all_tables:
        if table.id not in list_unav:
            available_tables.append(table)
    
    table_to_return = available_tables[0]

    return table_to_return


def confirm_availability(request_start, number_guests):     # Add request_start and number_guests param. later
    available_tables = get_available_tables(request_start)
    sum = 0

    for table in available_tables:
        sum = sum + table.size
    
    if sum >= number_guests:
        return available_tables
