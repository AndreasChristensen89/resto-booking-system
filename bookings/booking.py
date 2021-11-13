from .models import Booking, Table


def get_available_tables(request_start, number_guests):
    """
    This method returns the first available table of a restaurant, given a specific number of
    people and a booking date/time.
    """
    # request_start is string format, so we do some logic to change the two chars to +3
    # this works for reservations at 21:00
    full_string = list(request_start)
    end_integer = int(full_string[11] + full_string[12]) + 3
    full_string[11] = str(end_integer)[0]
    full_string[12] = str(end_integer)[1]
    request_end = "".join(full_string)
    
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
    # Currently only able to assign one table,
    # so one table is assigned according to group size using table's 
    available_tables = []
    all_tables = Table.objects.all()
    for table in all_tables:
        if table.id not in list_unav:
            if table.size == int(number_guests):
                available_tables.append(table)

    return available_tables


def confirm_availability(request_start, number_guests):     # Add request_start and number_guests param. later
    available_tables = get_available_tables(request_start)
    sum = 0

    for table in available_tables:
        sum = sum + table.size
    
    if sum >= number_guests:
        return available_tables
