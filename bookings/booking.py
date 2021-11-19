from datetime import datetime
from .models import Booking, Table, OpeningHours


def get_opening_hours(current_date_weekday):
    list_times = []
    opening_time = OpeningHours.objects.filter(
        weekday=current_date_weekday).values('from_time')
    closing_time = OpeningHours.objects.filter(
        weekday=current_date_weekday).values('to_time')
    for opening in opening_time:
        list_times.append(opening)
    for closing in closing_time:
        list_times.append(closing)
    extracted_times = []
    for time in range(len(list_times)):
        for key in list_times[time]:
            extracted_times.append(list_times[time][key])
    
    return extracted_times


def generate_request_end(request_start):
    # request_start is string format, so we do some logic to change the two chars to +3 hours
    # this works for reservations until 21:00
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
        elif abs(best_comb_3tables) <abs(best_comb_2tables):
            optimal_solution = fitting_tables_3tables

    return optimal_solution


def display_available_times(number_guests, date):
    date_weekday = datetime.strptime(date, '%Y-%m-%d %H:%M:%S').weekday()

    opens_closes = get_opening_hours(date_weekday)
    opening_time_str = str(opens_closes[0])[0:2]
    closing_time_str = str(opens_closes[1])[0:2]

    booking_interval = 30
    available_times = []

    for i in range(int(opening_time_str), int(closing_time_str)-2):
        time_to_test = ':00:00'
        start_to_pass = date + ' ' + str(i) + time_to_test
        available_tables = get_available_tables(start_to_pass)
        sum = 0
        for table in available_tables:
            sum += table.size
        if sum >= number_guests:
            available_times.append(f'{i}:00 ')
        if i < int(closing_time_str)-3:
            for minute in range(booking_interval, 60, booking_interval):
                time_to_add = str(minute)
                time_to_test = ':' + time_to_add + ':00'
                available_tables = get_available_tables(start_to_pass)
                sum = 0
                for table in available_tables:
                    sum += table.size
                if sum >= number_guests:
                    available_times.append(f'{i}:{minute} ')
    
    return available_times
