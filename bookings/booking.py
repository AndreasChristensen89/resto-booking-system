from .models import Booking, Table, OpeningHours
from datetime import datetime


def get_available_tables(request_start, number_guests):
    """
    This method returns the first available table of a restaurant, given a specific number of
    people and a booking date/time.
    """
    # request_start is string format, so we do some logic to change the two chars to +3 hours
    # this works for reservations until 21:00
    full_string = list(request_start)
    end_integer = int(full_string[11] + full_string[12]) + 3
    full_string[11] = str(end_integer)[0]
    full_string[12] = str(end_integer)[1]
    request_end = "".join(full_string)

    unavailable_tables = []

    # 1. Remove existing reserv. that have the same start-time
    tables_check_temp = Booking.objects.filter(
        booking_start=request_start).values('table')
    for table in tables_check_temp:
        unavailable_tables.append(table)

    # 2. Remove existing reserv. that start before request-start but finish after
    tables_check_temp_two = Booking.objects.filter(
        booking_start__lt=request_start,
        booking_end__gt=request_start).values('table')
    for table in tables_check_temp_two:
        unavailable_tables.append(table)

    # 3. Remove existing reserv. that start before and finish after request-end
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

    # Take all tables and sort out those with ids from the unavailable list
    available_tables = []
    all_tables = Table.objects.all()
    for table in all_tables:
        if table.id not in list_unav:
            available_tables.append(table)

    return available_tables


def confirm_availability(request_start, number_guests):
    available_tables = get_available_tables(request_start, number_guests)
    fitting_tables = []

    # will be used to calculate optimal table.size/combinations
    spots_to_fill = int(number_guests)

    # First check for exact table-size match
    for table in available_tables:
        if table.size == int(number_guests):
            fitting_tables.append(table)
            spots_to_fill = 0
            break
    # Second check for - seat - e.g. table for 6 for 5 people
    if spots_to_fill == number_guests:
        for table in available_tables:
            if table.size-1 == int(number_guests):
                fitting_tables.append(table)
                spots_to_fill = 0
                break

    # The following tests all combinations of 2 tables added together
    # The combination closest to 0 will be returned (least wasted space)
    # Currently only works for parties <= two largest tables put together

    # high number to be sure that new combination is lower
    best_combination = 100
    # how many seats gained/wasted. x < 0 == wasted
    seat_difference = 0

    if spots_to_fill == int(number_guests):
        for i in range(0, len(available_tables)-1):
            for j in range(i+1, len(available_tables)):
                combination = available_tables[i].size + available_tables[j].size
                seat_difference = int(number_guests)-combination
                if seat_difference <= 0 and abs(seat_difference) < abs(best_combination):
                    best_combination = seat_difference
                    fitting_tables = []
                    fitting_tables.append(available_tables[i])
                    fitting_tables.append(available_tables[j])

    return fitting_tables


def confirm_opening_hours(request_start):
    start_datetime = datetime.strptime(request_start, '%Y-%m-%d %H:%M')
    request_time = datetime.strptime(request_start, '%Y-%m-%d %H:%M').time()
    request_weekday = start_datetime.weekday()
    opening_hours = OpeningHours.objects.all()
    restaurant_open = False
    for day in opening_hours:
        if day.from_time <= request_time and day.weekday == request_weekday:
            restaurant_open = True
    return restaurant_open
