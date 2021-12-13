from datetime import timedelta
from .models import Booking, Table
from restaurant.models import OpeningHours, BookingDetails
import datetime

# (1, "Assign tables - same zone, only adjoining tables"),
# (2, "Assign tables - same zone, only adjoining but movables can be added"),
# (3, "Assign tables - same zone, any tables"),
# (4, "Assign tables - any available tables"), DONE

def return_tables(request_start, number_guests, sorting_method):
    available_tables = []
    
    if sorting_method == 0:
        available_tables == xx
    elif sorting_method == 1:
        available_tables = xx
    elif sorting_method == 2:
        available_tables == xx
    elif sorting_method == 3:
        available_tables == xx
    elif sorting_method == 4:
        available_tables == xx

    return available_tables

# tested
def get_opening_hours(weekday):
    if not isinstance(weekday, int):
        raise TypeError("Value needs to be an integer")
    opening_time = OpeningHours.objects.filter(
        weekday=weekday)

    return opening_time

# tested
def generate_request_end(request_start):
    duration = BookingDetails.objects.all()[0].booking_duration
    request_end = request_start + timedelta(minutes=duration)

    return request_end

# tested
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

# tested
def return_combination(available_tables):
    """
    This method takes the available tables and uses 3 step logic to sort the best combination
    1. Checks if there are exact group-table matches, or match-1 (size 6 for 5 people)
      1.a if not, best option is stored if it can fit the party
    2. Generates best two-table-combination, then same with three tables
    3. Compare best option for 1/2/3 combinations
      3.a hierarchy: fewest lost seats -> if equal: fewest tables used
    """
    

    # available_tables = get_available_tables(request_start)
    fitting_tables_1table = []
    fitting_tables_2tables = []
    fitting_tables_3tables = []
    optimal_solution = []

    # high number to be sure the following is lower
    best_comb_1table = 100
    best_comb_2tables = 100
    best_comb_3tables = 100

    spots_to_fill = number_guests

    # Step 1:
    # a. store best option is case no exact match
    # b. check for exact table-size match
    # c. Second check for -1 match
    for table in available_tables:
        seat_difference = number_guests-table.size
        if seat_difference <= 0 and abs(seat_difference) < abs(best_comb_1table):
            best_comb_1table = seat_difference
            fitting_tables_1table = []
            fitting_tables_1table.append(table)

            if table.size == number_guests:
                optimal_solution = []
                optimal_solution.append(table)
                spots_to_fill = 0
                break
            elif not optimal_solution and table.size-1 == number_guests:
                optimal_solution.append(table)
                spots_to_fill = 0

    # Step 2
    # Triggered if not exact match
    # 3 for loops. Second loop adds i+j, third i+j+k. Continuously updates lists
    if spots_to_fill == number_guests:
        for i in range(0, len(available_tables)-1):
            for j in range(i+1, len(available_tables)):
                combination = available_tables[i].size + available_tables[j].size
                seat_difference = number_guests-combination
                if seat_difference <= 0 and abs(seat_difference) < abs(best_comb_2tables):
                    best_comb_2tables = seat_difference
                    fitting_tables_2tables = []
                    fitting_tables_2tables.append(available_tables[i])
                    fitting_tables_2tables.append(available_tables[j])
                for k in range(j+1, len(available_tables)):
                    combination = available_tables[i].size + available_tables[j].size + available_tables[k].size
                    seat_difference = number_guests-combination
                    if seat_difference <= 0 and abs(seat_difference) < abs(best_comb_3tables):
                        best_comb_3tables = seat_difference
                        fitting_tables_3tables = []
                        fitting_tables_3tables.append(available_tables[i])
                        fitting_tables_3tables.append(available_tables[j])
                        fitting_tables_3tables.append(available_tables[k])
    
    # Step 3
    # All combinations are matched. Prefers fewest losses, then fewest tables
    if best_comb_1table <= 0 and abs(best_comb_1table) <= abs(best_comb_2tables):
        optimal_solution = fitting_tables_1table
    elif abs(best_comb_2tables) <= abs(best_comb_3tables):
        optimal_solution = fitting_tables_2tables
    elif abs(best_comb_3tables) < abs(best_comb_2tables):
        optimal_solution = fitting_tables_3tables

    if not optimal_solution:
        optimal_solution = sort_large_party(number_guests, available_tables)

    return optimal_solution

# tested
def sort_large_party(number_guests, av_tables):
    """
    Function activated if no three-table-combination can fit guests
    Adds tables sorted largest to smallest, won't add if sum exceeds number of guests
    Surplus tables are kept in case no exact match is found
    If no exact match will add the table that wastes the fewest seats
    """
    # sorting available tables, biggest first
    sorted = [av_tables[i].size >= av_tables[i+1].size for i in range(len(av_tables)-1)]

    if False in sorted:
        av_tables.sort(key=lambda x: x.size, reverse=True)
        # tables_sorted = sorted(av_tables, key=lambda x: x.size, reverse=True)

    table_combination = []
    check_two = []
    sum_seats = 0

    # Add biggest first, if sum passes guests it's not added
    # All tables that causes surplus are added to new list
    for table in av_tables:
        if sum_seats < number_guests:
            if sum_seats + table.size <= number_guests:
                table_combination.append(table)
                sum_seats += table.size
            else:
                check_two.append(table)
        else:
            break
    # if not perfect match it will run through the remains
    # add table that wastes the least seats
    if number_guests > sum_seats and check_two:
        check_two.sort(key=lambda x: x.size, reverse=False)
        difference = number_guests - sum_seats
        list_temp = []
        for table in check_two:
            if table.size == difference:
                table_combination.append(table)
                sum_seats += table.size
                break
            elif not list_temp or table.size < list_temp[0].size:
                list_temp = []
                list_temp.append(table)
        table_combination.append(list_temp[0])
        sum_seats += list_temp[0].size

    if sum_seats < number_guests:
        table_combination = []
    return table_combination

# tested
def test_time(request_start):
    if not isinstance(request_start, datetime.datetime):
        raise TypeError("Value needs to be datetime object")
    start_time = request_start.time()
    end = generate_request_end(request_start)
    end_time = end.time()
    weekday = request_start.weekday()

    opens_closes = get_opening_hours(weekday)
    opening_time = opens_closes[0].from_time
    closing_time = opens_closes[0].to_time

    within_hours = True

    if start_time < opening_time or end_time > closing_time or end_time < opening_time:
        within_hours = False

    return within_hours

# tested
def double_booking(request_start, user):

    request_end = generate_request_end(request_start)
    
    check_one = Booking.objects.filter(
        author=user,
        booking_start=request_start)

    check_two = Booking.objects.filter(
        author=user,
        booking_start__lt=request_start,
        booking_end__gt=request_start)

    check_three = Booking.objects.filter(
        author=user,
        booking_start__lt=request_end,
        booking_end__gt=request_end)

    conflicting = len(check_one) + len(check_two) + len(check_three)

    return conflicting
