from django.test import TestCase
from django.contrib.auth.models import User
from restaurant.models import OpeningHours, BookingDetails
from .booking import get_opening_hours, generate_request_end, get_available_tables, return_tables
from .models import Booking, Table
import datetime


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
        BookingDetails.objects.create(
            booking_duration=180,
            auto_table_assign=True
        )
        returned_datetime = generate_request_end(datetime.datetime(2021, 12, 12, 10, 0))
        self.assertEqual(returned_datetime, datetime.datetime(2021, 12, 12, 13, 0))

    def test_no_value_is_passed_into_function(self):
        self.assertRaises(TypeError, generate_request_end)

    def test_wrong_value_is_passed_into_function(self):
        BookingDetails.objects.create(
            booking_duration=180,
            auto_table_assign=True
        )
        self.assertRaises(TypeError, generate_request_end, 1)


class TestGetAvailableTables(TestCase):
    
    def test_all_tables_returned(self):
        create_duration = BookingDetails.objects.create(
            booking_duration=180,
            auto_table_assign=True
        )
        Table.objects.create(size=2)
        Table.objects.create(size=2)
        Table.objects.create(size=4)
        Table.objects.create(size=4)
        tables = get_available_tables(datetime.datetime(2021, 12, 12, 10, 0))
        self.assertEqual(len(tables), 4)

    def test_does_not_returned_booked_table(self):
        BookingDetails.objects.create(
            booking_duration=180,
            auto_table_assign=True
        )
        create_table = Table.objects.create(size=2)
        create_table = Table.objects.create(size=2)
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
        tables_returned = get_available_tables(datetime.datetime(2021, 11, 6, 12, 0))
        self.assertEqual(len(tables_returned), 1)

    def test_only_returns_if_outside_duration(self):
        BookingDetails.objects.create(
            booking_duration=180,
            auto_table_assign=True
        )
        Table.objects.create(size=2)
        Table.objects.create(size=2)
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

        tables_returned_nine = get_available_tables(datetime.datetime(2021, 11, 6, 9, 0))
        tables_returned_ten = get_available_tables(datetime.datetime(2021, 11, 6, 10, 0))
        tables_returned_eleven = get_available_tables(datetime.datetime(2021, 11, 6, 11, 0))
        tables_returned_twelve = get_available_tables(datetime.datetime(2021, 11, 6, 12, 0))
        tables_returned_thirteen = get_available_tables(datetime.datetime(2021, 11, 6, 13, 0))
        tables_returned_fourteen = get_available_tables(datetime.datetime(2021, 11, 6, 14, 0))
        tables_returned_fifteen = get_available_tables(datetime.datetime(2021, 11, 6, 15, 0))

        self.assertEqual(len(tables_returned_nine), 2)
        self.assertEqual(len(tables_returned_ten), 1)
        self.assertEqual(len(tables_returned_eleven), 1)
        self.assertEqual(len(tables_returned_twelve), 1)
        self.assertEqual(len(tables_returned_thirteen), 1)
        self.assertEqual(len(tables_returned_fourteen), 1)
        self.assertEqual(len(tables_returned_fifteen), 2)


class TestReturnTables(TestCase):
    def test_sum_of_seat_loss_never_less_than_two(self):
        BookingDetails.objects.create(
            booking_duration=180,
            auto_table_assign=True
        )
        for i in range(4):
            Table.objects.create(size=2)
        for i in range(3):
            Table.objects.create(size=4)
        for i in range(2):
            Table.objects.create(size=6)
        for i in range(1):
            Table.objects.create(size=8)
        request_start = datetime.datetime(2021, 11, 6, 9, 0)

        for i in range(1, 15):
            tables_returned = return_tables(request_start, i)
            sum = 0
            for table in tables_returned:
                sum += table.size
            self.assertLess(sum, i+2)
