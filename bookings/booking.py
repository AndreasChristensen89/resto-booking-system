from datetime import datetime, timedelta
from .models import Booking, Table, OpeningHours, BookingDetails


def get_opening_hours(current_date_weekday):
    opening_time = OpeningHours.objects.filter(
        weekday=current_date_weekday)

    return opening_time


def generate_request_end(request_start):
    # request_start is string format, so we do some logic to change the two chars to +3 hours
    # this works for reservations until 21:00
    # Add bookingDetails model instead of +3
    full_string = list(request_start)
    end_integer = int(full_string[11] + full_string[12]) + 3
    full_string[11] = str(end_integer)[0]
    full_string[12] = str(end_integer)[1]
    request_end = "".join(full_string)

    return request_end


def get_available_tables(request_start):
    """
    This method returns the first available table(s) of the restaurant
    """
    request_end = generate_request_end(request_start)
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


def return_tables(request_start, number_guests):
    # This method takes the available tables and uses 3 step logic to sort the best combination
    # 1. Checks if there exact group-table matches, or match-1 (size 6 for 5 people)
    #   1.a if not, best option is stored
    # 2. Generates best two-table-combination, then same with three tables
    # 3. Compare best option for 1/2/3 combinations
    #   3.a hierarchy: fewest lost seats -> if equal: fewest tables used

    available_tables = get_available_tables(request_start)
    fitting_tables_1table = []
    fitting_tables_2tables = []
    fitting_tables_3tables = []
    optimal_solution = []

     # high number to be sure the following is lower
    best_comb_1table = 100
    best_comb_2tables = 100
    best_comb_3tables = 100

    spots_to_fill = int(number_guests)

    # Step 1:
    # a. store best option is case no exact match
    # b. check for exact table-size match
    # c. Second check for -1 match
    for table in available_tables:
        seat_difference = int(number_guests)-table.size
        if seat_difference <= 0 and abs(seat_difference) < abs(best_comb_1table):
            best_comb_1table = seat_difference
            fitting_tables_1table = []
            fitting_tables_1table.append(table)

            if table.size == int(number_guests):
                optimal_solution = []
                optimal_solution.append(table)
                spots_to_fill = 0
                break
            elif not optimal_solution and table.size-1 == int(number_guests):
                optimal_solution.append(table)
                spots_to_fill = 0

    # Step 2
    # Triggered if not exact match
    # 3 for loops. Second loop adds i+j, third i+j+k. Continuously updates lists
    if spots_to_fill == int(number_guests):
        for i in range(0, len(available_tables)-1):
            for j in range(i+1, len(available_tables)):
                combination = available_tables[i].size + available_tables[j].size
                seat_difference = int(number_guests)-combination
                if seat_difference <= 0 and abs(seat_difference) < abs(best_comb_2tables):
                    best_comb_2tables = seat_difference
                    fitting_tables_2tables = []
                    fitting_tables_2tables.append(available_tables[i])
                    fitting_tables_2tables.append(available_tables[j])
                for k in range(j+1, len(available_tables)):
                    combination = available_tables[i].size + available_tables[j].size + available_tables[k].size
                    seat_difference = int(number_guests)-combination
                    if seat_difference <= 0 and abs(seat_difference) < abs(best_comb_3tables):
                        best_comb_3tables = seat_difference
                        fitting_tables_3tables = []
                        fitting_tables_3tables.append(available_tables[i])
                        fitting_tables_3tables.append(available_tables[j])
                        fitting_tables_3tables.append(available_tables[k])
        # Step 3
        # All combinations are matched. Prefers fewest losses, then fewest tables

        if abs(best_comb_1table) <= abs(best_comb_2tables):
            optimal_solution = fitting_tables_1table
        elif abs(best_comb_2tables) <= abs(best_comb_3tables):
            optimal_solution = fitting_tables_2tables
        elif abs(best_comb_3tables) < abs(best_comb_2tables):
            optimal_solution = fitting_tables_3tables
    
    if not optimal_solution:
        optimal_solution = sort_large_party(request_start, number_guests, available_tables)

    return optimal_solution


def sort_large_party(request_start, number_guests, available_tables):
    available_tables.sort(key=lambda x: x.size, reverse=True)
    tables_sorted = sorted(available_tables, key=lambda x: x.size, reverse=True)

    table_combination = []
    sum = 0
    for table in tables_sorted:
        if sum < number_guests:
            table_combination.append(table)
            sum += table.size
    if sum < number_guests:
        table_combination = []
    
    return table_combination


def test_available_times(request_start, number_guests):
    start = datetime.strptime(request_start, '%Y-%m-%d %H:%M:%S')
 
    start_time = start.time()   # 17:00:00
    duration = BookingDetails.objects.all()[0].booking_duration_minutes
    end = start + timedelta(minutes=duration)   # 180
    end_time = end.time()       # 20:00:00

    opens_closes = get_opening_hours(start.weekday())  # 10:00:0023:00:00
    opening_time = opens_closes[0].from_time
    closing_time = opens_closes[0].to_time

    available_tables = False
    availability_check = []

    if start_time >= opening_time and end_time <= closing_time:
        availability_check = get_available_tables(request_start)
        sum = 0
        for table in availability_check:
            sum += table.size
        if sum >= number_guests:
            available_tables = True
    
    return available_tables


def number_of_guests(request_start):
    bookings = Booking.objects.filter(
        booking_start=request_start)
    sum_guests = 0
    for booking in bookings:
        sum_guests += booking.number_guests

    return sum_guests