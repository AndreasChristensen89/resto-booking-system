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
            available_tables.append(table)

    return available_tables


def confirm_availability(request_start, number_guests):     # Add request_start and number_guests param. later
    available_tables = get_available_tables(request_start, number_guests)
    fitting_tables = []

    # Runs through all tables starting length of number_guests, adds first table that is closest in size
    # e.g. number_guests == 8 -> check for 8, 7, 6(hit) -> add table size 6
    
    spots_to_fill = int(number_guests)

    # table id registered to avoid using same table twice
    table_id = 0
    
    # Reverse for loop to get first available table with size closest to number_guests
    for i in range(int(number_guests), 1, -1):
        for table in available_tables:
            if table.size == i:
                fitting_tables.append(table)
                spots_to_fill -= table.size
                table_id = table.id
                break
        # My idea is to create for loop that for each round adds the size of next table to itself
        # This sum is stored as a value in a list, and the loop continues with the next table
        # In the end we have a list with the sum of each combination
        # We subtract the guest number with each combination,
        # and the smallest number is the most optimal comb. to return
        # if spots_to_fill == int(number_guests):
        #     def create_combination():
        #         sum = 0
        #         combinations = []
        #         for table in available_tables:
        #             while sum < int(number_guests):

        #                 if table.size-1 == int(number_guests):
        #                     fitting_tables.append(table)
        #                     spots_to_fill -= table.size
        #                     table_id = table.id
        #                     break
        #     if spots_to_fill < int(number_guests):
        #     break
    
    # For loop in range to find table equal to spots_to_fill, or closest larger table
    for i in range(spots_to_fill, 11):
        if spots_to_fill > 0:
            for table in available_tables:
                if table.size == i and table.id is not table_id:
                    fitting_tables.append(table)
                    spots_to_fill -= int(table.size)
                    break
            if spots_to_fill <= 0:
                break
    
    return fitting_tables
