from django.test import TestCase
from .models import OpeningHours, BookingDetails
import datetime


class TestOpeningHours(TestCase):

    def test_objects_can_be_made(self):
        OpeningHours.objects.create(
            weekday=1,
            from_time=datetime.time(10, 00),
            to_time=datetime.time(22, 00),
        )
        self.assertEqual(OpeningHours.objects.all().count(), 1)
        self.assertEqual(OpeningHours.objects.all()[0].weekday, 1)


class TestBookingDetails(TestCase):

    def test_objects_are_created(self):
        BookingDetails.objects.create(
            booking_duration=120,
            table_assign_method=1,
            assign_method_limit=50,
        )
        self.assertEqual(BookingDetails.objects.all().count(), 1)
        self.assertEqual(BookingDetails.objects.all()[0].booking_duration, 120)
        self.assertEqual(BookingDetails.objects.all()[0].table_assign_method, 1)
        self.assertEqual(BookingDetails.objects.all()[0].assign_method_limit, 50)

    def test_assign_limit_automatically_100(self):
        BookingDetails.objects.create(
            booking_duration=120,
            table_assign_method=1,
        )
        self.assertEqual(BookingDetails.objects.all()[0].assign_method_limit, 100)
