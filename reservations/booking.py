from datetime import timedelta
from .models import Booking, Table
from restaurant.models import OpeningHours, BookingDetails
import datetime


def return_tables(request_start, nbr_guests, sort_method):
    """
    Function that redirects to correct sorting method
    and returns best combination of tables
    """

    request_end = generate_request_end(request_start)
    solution = []
    av_tables = return_all_available_tables(request_start, request_end)
    if sort_method == 1:
        solution = table_method_same_zone(av_tables, nbr_guests, sort_method)
    elif sort_method == 2:
        solution = return_combination(av_tables, nbr_guests)

    return solution


def table_method_same_zone(available_tables, number_guests, sorting_method):
    """
    Returns any available tables from the same zone
    Tests list of each zone in return_combinations()
    Favors fewest losses
    """

    list_of_zones = []
    for table in available_tables:
        if table.zone not in list_of_zones:
            list_of_zones.append(table.zone)
    tables_to_return = []
    fewest_losses = 100

    for zone in list_of_zones:
        tables_in_zone = []
        sum = 0
        for table in available_tables:
            if table.zone == zone:
                tables_in_zone.append(table)
                sum += table.seats
        if sum >= number_guests:
            zone_losses = number_guests
            result_zone = return_combination(tables_in_zone, number_guests)
            for table in result_zone:
                zone_losses -= table.seats
            if abs(fewest_losses) > abs(zone_losses):
                fewest_losses = zone_losses
                tables_to_return = result_zone

    return tables_to_return


def return_all_available_tables(request_start, request_end):
    """
    Returns any available tables
    Three types of overlap are filtered:
    1. Same start 2. Starts before & ends during 3. Starts before end
    Removes overlap tables from list of all tables
    """
    unavailable_tables = []

    tables_check_temp = Booking.objects.filter(
        booking_start=request_start).values('table')
    for table in tables_check_temp:
        unavailable_tables.append(table)

    tables_check_temp_two = Booking.objects.filter(
        booking_start__lt=request_start,
        booking_end__gt=request_start).values('table')
    for table in tables_check_temp_two:
        unavailable_tables.append(table)

    tables_check_temp_three = Booking.objects.filter(
        booking_start__lt=request_end,
        booking_end__gt=request_end).values('table')
    for table in tables_check_temp_three:
        unavailable_tables.append(table)

    list_unav = []
    for table in range(len(unavailable_tables)):
        for key in unavailable_tables[table]:
            list_unav.append(unavailable_tables[table][key])

    available_tables = []
    all_tables = Table.objects.all()
    for table in all_tables:
        if table.id not in list_unav:
            available_tables.append(table)

    return available_tables


def return_combination(av_tables, number_guests):
    """
    Takes available tables and uses 3 step logic to sort the best combination
    1. Checks for exact group-table matches, or match-1 (6 seats for 5 people)
      1.a if not, best option is stored if it can fit the party
    2. Generates best two-table-combination, then same with three tables
    3. Compare best option for 1/2/3 combinations
      3.a hierarchy: fewest lost seats -> if equal: fewest tables used
    """

    fitting_tables_1table = []
    fitting_tables_2tables = []
    fitting_tables_3tables = []
    optimal_solution = []

    comb_1table = 100
    comb_2tables = 100
    comb_3tables = 100

    spots_to_fill = number_guests

    for table in av_tables:
        seat_dif = number_guests-table.seats
        if seat_dif <= 0 and abs(seat_dif) < abs(comb_1table):
            comb_1table = seat_dif
            fitting_tables_1table = []
            fitting_tables_1table.append(table)

            if table.seats == number_guests:
                optimal_solution = []
                optimal_solution.append(table)
                spots_to_fill = 0
                break
            elif not optimal_solution and table.seats-1 == number_guests:
                optimal_solution.append(table)
                spots_to_fill = 0

    if spots_to_fill == number_guests:
        for i in range(0, len(av_tables)-1):
            for j in range(i+1, len(av_tables)):
                comb = av_tables[i].seats + av_tables[j].seats
                seat_dif = number_guests-comb
                if seat_dif <= 0 and abs(seat_dif) < abs(comb_2tables):
                    comb_2tables = seat_dif
                    fitting_tables_2tables = []
                    fitting_tables_2tables.append(av_tables[i])
                    fitting_tables_2tables.append(av_tables[j])
                for k in range(j+1, len(av_tables)):
                    comb = av_tables[i].seats + av_tables[j].seats + av_tables[k].seats
                    seat_dif = number_guests-comb
                    if seat_dif <= 0 and abs(seat_dif) < abs(comb_3tables):
                        comb_3tables = seat_dif
                        fitting_tables_3tables = []
                        fitting_tables_3tables.append(av_tables[i])
                        fitting_tables_3tables.append(av_tables[j])
                        fitting_tables_3tables.append(av_tables[k])

    if comb_1table <= 0 and abs(comb_1table) <= abs(comb_2tables):
        optimal_solution = fitting_tables_1table
    elif abs(comb_2tables) <= abs(comb_3tables):
        optimal_solution = fitting_tables_2tables
    elif abs(comb_3tables) < abs(comb_2tables):
        optimal_solution = fitting_tables_3tables

    if not optimal_solution:
        optimal_solution = sort_large_party(number_guests, av_tables)

    return optimal_solution


def sort_large_party(number_guests, av_tables):
    """
    Function activated if no three-table-combination can fit guests.
    Adds tables sorted largest to smallest,
    won't add if sum exceeds number of guests.
    Surplus tables are kept in case no exact match is found.
    If no exact match will add the table that wastes the fewest seats.
    """

    sorted = [av_tables[i].seats >= av_tables[i+1].seats for i in range(len(av_tables)-1)]

    if False in sorted:
        av_tables.sort(key=lambda x: x.seats, reverse=True)

    table_combination = []
    check_two = []
    sum_seats = 0

    for table in av_tables:
        if sum_seats < number_guests:
            if sum_seats + table.seats <= number_guests:
                table_combination.append(table)
                sum_seats += table.seats
            else:
                check_two.append(table)
        else:
            break

    if number_guests > sum_seats and check_two:
        check_two.sort(key=lambda x: x.seats, reverse=False)
        difference = number_guests - sum_seats
        list_temp = []
        for table in check_two:
            if table.seats == difference:
                table_combination.append(table)
                sum_seats += table.seats
                break
            elif not list_temp or table.seats < list_temp[0].seats:
                list_temp = []
                list_temp.append(table)
        table_combination.append(list_temp[0])
        sum_seats += list_temp[0].seats

    if sum_seats < number_guests:
        table_combination = []
    return table_combination


def test_time(request_start):
    """
    Function that takes the opening hours for the weekday of the booking_start
    Matches the stated hours with the request and returns a boolean
    """

    if not isinstance(request_start, datetime.datetime):
        raise TypeError("Value needs to be datetime object")
    start = request_start.time()
    end = generate_request_end(request_start)
    end_time = end.time()
    weekday = request_start.weekday()

    opens_closes = get_opening_hours(weekday)
    opening = opens_closes[0].from_time
    closing = opens_closes[0].to_time

    within_hours = True

    if start < opening or end_time > closing or end_time < opening:
        within_hours = False

    return within_hours


def double_booking(request_start, user):
    """
    Functions that checks if user has already booked
    in an overlapping time period
    """
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


def get_opening_hours(weekday):
    """
    Returns the opening hours of the datetime entered in form
    """
    if not isinstance(weekday, int):
        raise TypeError("Value needs to be an integer")
    opening_time = OpeningHours.objects.filter(
        weekday=weekday)

    return opening_time


def generate_request_end(request_start):
    """
    Generates an ending time of the booking
    according to what admin has set in booking details
    """

    duration = BookingDetails.objects.all()[0].booking_duration
    request_end = request_start + timedelta(minutes=duration)

    return request_end
