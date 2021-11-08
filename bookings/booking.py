

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


def get_available_tables(request_start, number_guests):
    """
    This method returns the first available table of a restaurant, given a specific number of
    people and a booking date/time.
    """
    delta = timedelta(seconds=60*180)
    request_end = request_start + delta
    
    unavailable_tables = []

    # Exclude tables that have the same start time
    tables_check_temp = Booking.objects.filter(
        booking_start=request_start).values('table')
    for table in tables_check_temp:
        unavailable_tables.append(table)
    
    # Exclude tables that start before requested start + end after requested start
    tables_check_temp = Booking.objects.filter(
        booking_start__lt=request_start,
        booking_end__gt=request_start).values('table')
    for table in tables_check_temp:
        unavailable_tables.append(table)
    
    # Exclude tables that start before end of request + end after end of request
    tables_check_temp = Booking.objects.filter(
        booking_start__lt=request_end,
        booking_end__gt=request_end).values('table')
    for table in tables_check_temp:
        unavailable_tables.append(table)

    # Take all tables and remove the ones from unavailable_tables
    tables = Table.objects.all()
    for table in tables:
        if table in unavailable_tables:
            tables.remove(table)
    
    return tables


def confirm_availability(request_start, number_guests):
    available_tables = get_available_tables(request_start, number_guests)
    sum = 0

    for table in available_tables:
        sum += table.size
    
    if sum < number_guests:
        print(sum)
        return False
    else:
        return True