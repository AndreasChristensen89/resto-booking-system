from django.test import TestCase
from django.contrib.auth.models import User
from restaurant.models import OpeningHours, BookingDetails
from reservations.booking import *
from .models import Booking, Table
from .test_forms import create_booking_details, create_booking_form
import datetime


class TestReturnTables(TestCase):

    def test_only_same_zone_returned(self):
        booking_details = create_booking_details(1)
        Table.objects.create(table_number=1, seats=2, zone=1, moveable=False)
        Table.objects.create(table_number=2, seats=2, zone=2, moveable=False)
        Table.objects.create(table_number=3, seats=4, zone=3, moveable=False)
        tables_for_two = return_tables(datetime.datetime(2021, 12, 12, 10, 0), 2, 1)
        tables_for_four = return_tables(datetime.datetime(2021, 12, 12, 10, 0), 4, 1)
        self.assertEqual(len(tables_for_two), 1)
        self.assertEqual(len(tables_for_four), 1)
    
    def test_returns_tables_from_different_zones(self):
        booking_details = create_booking_details(2)
        Table.objects.create(table_number=1, seats=2, zone=1, moveable=False)
        Table.objects.create(table_number=2, seats=2, zone=2, moveable=False)
        Table.objects.create(table_number=3, seats=4, zone=3, moveable=False)
        all_tables = return_tables(datetime.datetime(2021, 12, 12, 10, 0), 8, 2)
        self.assertEqual(len(all_tables), 3)
        

class TestGetOpeningHours(TestCase):

    def test_return_correct_times(self):
        OpeningHours.objects.create(
            weekday=1,
            from_time='10:00',
            to_time='22:00'
            )
        OpeningHours.objects.create(
            weekday=2,
            from_time='09:00',
            to_time='16:00'
            )
        opening_hours_return = get_opening_hours(1)
        self.assertEqual(opening_hours_return[0].from_time, datetime.time(10, 0))
        self.assertEqual(opening_hours_return[0].to_time, datetime.time(22, 0))
        self.assertEqual(opening_hours_return[0].weekday, 1)

    def test_no_hours_to_return(self):
        opening_hours_return = get_opening_hours(1)
        self.assertEqual(len(opening_hours_return), 0)

    def test_function_returns_typeerror_if_wrong_value_is_passed_in(self):
        self.assertRaises(TypeError, get_opening_hours, 'test')

    def test_function_returns_error_if_no_parameter_is_passed(self):
        self.assertRaises(TypeError, get_opening_hours)


class TestGenerateRequestEnd(TestCase):
    
    def test_correct_datetime_is_returned(self):
        booking_details = create_booking_details(1)
        returned_datetime = generate_request_end(datetime.datetime(2021, 12, 12, 10, 0))
        self.assertEqual(returned_datetime, datetime.datetime(2021, 12, 12, 13, 0))

    def test_no_value_is_passed_into_function(self):
        self.assertRaises(TypeError, generate_request_end)

    def test_wrong_value_is_passed_into_function(self):
        booking_details = create_booking_details(1)
        self.assertRaises(TypeError, generate_request_end, 1)


class TestReturnAllAvailableTables(TestCase):
    
    def test_all_tables_returned(self):
        booking_details = create_booking_details(1)
        Table.objects.create(table_number=1, seats=2, zone=1, moveable=False)
        Table.objects.create(table_number=2, seats=2, zone=2, moveable=False)
        Table.objects.create(table_number=3, seats=4, zone=3, moveable=False)
        Table.objects.create(table_number=4, seats=4, zone=4, moveable=False)
        tables = return_all_available_tables(datetime.datetime(2021, 12, 12, 10, 0), datetime.datetime(2021, 12, 12, 13, 0))
        self.assertEqual(len(tables), 4)

    def test_does_not_returned_occupied_table(self):
        booking_details = create_booking_details(1)
        Table.objects.create(table_number=1, seats=2, zone=1, moveable=False)
        Table.objects.create(table_number=2, seats=2, zone=1, moveable=False)
        create_user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        create_booking = Booking.objects.create(
            first_name='x',
            last_name='x', 
            author=create_user, 
            number_guests=2, 
            booking_start='2021-11-06 12:00:00',
            booking_end='2021-11-06 15:00:00')
        tables = Table.objects.all()
        create_booking.table.add(tables[0])
        tables_returned = return_all_available_tables(datetime.datetime(2021, 11, 6, 12, 0), datetime.datetime(2021, 11, 6, 15, 0))
        self.assertEqual(len(tables_returned), 1)

    def test_only_returns_if_outside_duration(self):
        booking_details = create_booking_details(1)
        Table.objects.create(table_number=1, seats=2, zone=1, moveable=False)
        Table.objects.create(table_number=2, seats=2, zone=1, moveable=False)
        create_user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        create_booking = Booking.objects.create(
            first_name='x',
            last_name='x', 
            author=create_user, 
            number_guests=4, 
            booking_start='2021-11-06 12:00:00',
            booking_end='2021-11-06 15:00:00')
        tables = Table.objects.all()
        create_booking.table.add(tables[0])

        for i in range(10, 15):
            tables_returned = return_all_available_tables(datetime.datetime(2021, 11, 6, i, 0), datetime.datetime(2021, 11, 6, i+3, 0))
            self.assertEqual(len(tables_returned), 1)
        for i in range(9, 17, 6):
            tables_returned = return_all_available_tables(datetime.datetime(2021, 11, 6, i, 0), datetime.datetime(2021, 11, 6, i+3, 0))
            self.assertEqual(len(tables_returned), 2)

    def test_no_value_is_passed_into_function(self):
        self.assertRaises(TypeError, return_all_available_tables)


class TestReturnCombination(TestCase):
    
    def test_sum_of_seat_is_always_greater_or_equal_to_guests_method_one(self):
        booking_details = create_booking_details(1)
        for i in range(4):
            Table.objects.create(table_number=i, seats=2, zone=1, moveable=False)
        for i in range(3):
            Table.objects.create(table_number=4+i, seats=4, zone=1, moveable=False)
        for i in range(2):
            Table.objects.create(table_number=7+i, seats=6, zone=1, moveable=False)
        Table.objects.create(table_number=9, seats=8, zone=1, moveable=False)

        all_tables = Table.objects.all()
        table_list = [table for table in all_tables]
        request_start = datetime.datetime(2021, 11, 6, 12, 0)

        for i in range(1, 21):
            returned_tables = return_tables(request_start, i, 1)
            tables_returned = return_combination(returned_tables, i)
            sum = 0
            for table in tables_returned:
                sum += table.seats
            self.assertGreaterEqual(sum, i)
    
    def test_sum_of_seat_is_always_greater_or_equal_to_guests_method_two(self):
        booking_details = create_booking_details(2)
        for i in range(4):
            Table.objects.create(table_number=i, seats=2, zone=1, moveable=False)
        for i in range(3):
            Table.objects.create(table_number=4+i, seats=4, zone=1, moveable=False)
        for i in range(2):
            Table.objects.create(table_number=7+i, seats=6, zone=1, moveable=False)
        Table.objects.create(table_number=9, seats=8, zone=1, moveable=False)

        all_tables = Table.objects.all()
        table_list = [table for table in all_tables]
        request_start = datetime.datetime(2021, 11, 6, 12, 0)

        for i in range(1, 21):
            returned_tables = return_tables(request_start, i, 2)
            tables_returned = return_combination(returned_tables, i)
            sum = 0
            for table in tables_returned:
                sum += table.seats
            self.assertGreaterEqual(sum, i)

    def test_function_prefers_fewer_tables_used(self):
        booking_details = create_booking_details(2)
        Table.objects.create(table_number=1, seats=4, zone=1, moveable=False)
        Table.objects.create(table_number=2, seats=3, zone=1, moveable=False)
        Table.objects.create(table_number=3, seats=2, zone=1, moveable=False)
        Table.objects.create(table_number=4, seats=3, zone=1, moveable=False)
        Table.objects.create(table_number=5, seats=6, zone=1, moveable=False)
        request_start = datetime.datetime(2021, 11, 6, 9, 0)

        returned_tables_one = return_tables(request_start, 9, 1)
        returned_tables_two = return_tables(request_start, 9, 2)
        tables_returned_one = return_combination(returned_tables_one, 9)
        tables_returned_two = return_combination(returned_tables_two, 9)
        self.assertEqual(len(tables_returned_one), 2)
        self.assertEqual(len(tables_returned_two), 2)
        self.assertEqual(tables_returned_one[0].seats, 3)
        self.assertEqual(tables_returned_one[1].seats, 6)
        self.assertEqual(tables_returned_two[0].seats, 3)
        self.assertEqual(tables_returned_two[1].seats, 6)

    def test_function_returns_error_if_no_parameters_are_passed(self):
        self.assertRaises(TypeError, return_combination)

    def test_function_return_error_if_arguments_are_missing(self):
        self.assertRaises(TypeError, return_combination, 5)

    def test_function_return_error_if_integer_is_missing(self):
        booking_details = create_booking_details(1)
        Table.objects.create(table_number=1, seats=4, zone=1, moveable=False)
        Table.objects.create(table_number=2, seats=3, zone=2, moveable=False)
        Table.objects.create(table_number=3, seats=2, zone=3, moveable=False)
        Table.objects.create(table_number=4, seats=3, zone=4, moveable=False)
        Table.objects.create(table_number=5, seats=6, zone=5, moveable=False)
        request_start = datetime.datetime(2021, 11, 6, 9, 0)

        returned_tables = return_tables(request_start, 9, 1)
        self.assertRaises(TypeError, return_combination, datetime.datetime(2021, 12, 12, 13, 0))


class TestSortLargerParty(TestCase):
    
    def test_function_return_error_if_no_argument(self):
        self.assertRaises(TypeError, sort_large_party)
    
    def test_sum_of_seats_always_greater_or_equal_to_guests(self):
        booking_details = create_booking_details(1)
        for i in range(4):
            Table.objects.create(table_number=i, seats=2, zone=1, moveable=False)
        for i in range(3):
            Table.objects.create(table_number=4+i, seats=4, zone=1, moveable=False)
        for i in range(2):
            Table.objects.create(table_number=7+i, seats=6, zone=1, moveable=False)
        Table.objects.create(table_number=9, seats=8, zone=1, moveable=False)
        
        request_start = datetime.datetime(2021, 11, 6, 12, 0)
        request_end = datetime.datetime(2021, 11, 6, 15, 0)
        av_tables = return_all_available_tables(request_start, request_end)
        for i in range(1, 41):
            sum = 0
            returned_tables = sort_large_party(i, av_tables)
            for table in returned_tables:
                sum += table.seats 
            self.assertGreaterEqual(sum, i)

    def test_return_no_tables_if_not_enough(self):
        booking_details = create_booking_details(1)

        for i in range(4):
            Table.objects.create(table_number=i+1, seats=2, zone=1, moveable=False)

        request_start = datetime.datetime(2021, 11, 6, 12, 0)
        request_end = datetime.datetime(2021, 11, 6, 15, 0)
        av_tables = return_all_available_tables(request_start, request_end)
        returned_tables = sort_large_party(9, av_tables)
        self.assertEqual(len(returned_tables), 0)


class TestTestTime(TestCase):

    def test_returns_error_if_no_value_passed(self):
        self.assertRaises(TypeError, test_time)

    def test_returns_error_if_wrong_value_passed(self):
        self.assertRaises(TypeError, test_time, 2)
    
    def test_returns_correct_boolean(self):
        booking_details = create_booking_details(1)
        OpeningHours.objects.create(
            weekday=5,
            from_time='09:00',
            to_time='16:00')
        for i in range(9, 14):
            create_datetime = datetime.datetime(2021, 11, 6, i, 0)
            within_hours = test_time(create_datetime)
            self.assertEqual(within_hours, True)
        for i in range(14, 23):
            create_datetime = datetime.datetime(2021, 11, 6, i, 0)
            within_hours = test_time(create_datetime)
            self.assertEqual(within_hours, False)
        for i in range(0, 8):
            create_datetime = datetime.datetime(2021, 11, 6, i, 0)
            within_hours = test_time(create_datetime)
            self.assertEqual(within_hours, False)


class TestDoubleBooking(TestCase):

    def test_returns_error_if_no_value_passed(self):
        self.assertRaises(TypeError, double_booking)

    def test_returns_error_if_wrong_value_passed(self):
        self.assertRaises(TypeError, double_booking, 2)

    def test_returns_correct_number(self):
        booking_details = create_booking_details(1)

        conflicting_start = datetime.datetime(2021, 11, 6, 12, 0)
        non_conflicting_start = datetime.datetime(2021, 11, 7, 12, 0)

        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        booking = Booking.objects.create(
            first_name='x',
            last_name='x', 
            author=user, 
            number_guests=4, 
            booking_start='2021-11-06 12:00:00',
            booking_end='2021-11-06 15:00:00')

        conflicting_booking = double_booking(conflicting_start, user)
        non_conflicting_booking = double_booking(non_conflicting_start, user)

        self.assertEqual(conflicting_booking, 1)
        self.assertEqual(non_conflicting_booking, 0)


class TestTableMethodSameZone(TestCase):
    def test_list_of_zones(self):
        for i in range(4):
            Table.objects.create(table_number=i+1, seats=6, zone=1, moveable=True)
        for i in range(3):
            Table.objects.create(table_number=5+i, seats=4, zone=2, moveable=False)
        for i in range(2):
            Table.objects.create(table_number=8+i, seats=2, zone=3, moveable=True)
        Table.objects.create(table_number=10, seats=8, zone=4, moveable=False)
        request_start = datetime.datetime(2021, 11, 7, 12, 0)
        request_end = datetime.datetime(2021, 11, 7, 15, 0)
        available_tables  = return_all_available_tables(request_start, request_end)

        test_of_zones = table_method_same_zone(available_tables, 9, 3)
        self.assertEqual(len(test_of_zones), 2)