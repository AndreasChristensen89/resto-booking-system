from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from restaurant.models import BookingDetails
import random
import string


class Table(models.Model):
    table_number = models.IntegerField(unique=True, default=1)
    seats = models.IntegerField()
    zone = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return f'Table {self.table_number} - Seats: {self.seats} - Zone: {self.zone}'


class Booking(models.Model):
    STATUS = ((0, "Pending"), (1, "Approved"), (2, "Declined"))

    slug = models.SlugField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='table_booking')
    number_guests = models.PositiveIntegerField()
    booking_start = models.DateTimeField()
    booking_end = models.DateTimeField()
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    comment = models.TextField(max_length=200, blank=True)
    table = models.ManyToManyField(Table, related_name='booking_tables', blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            letters = string.ascii_lowercase
            random_str = ''.join(random.choice(letters) for i in range(5))
            self.slug = random_str
        super().save(*args, **kwargs)

    @property
    def is_past_due(self):
        return datetime.now() > self.booking_end

    @property
    def latest_cancellation(self):
        now = datetime.now()
        latest_cancel = self.booking_start - timedelta(minutes=120)
        return now <= latest_cancel

    class Meta:
        ordering = ["-created_on"]

    def get_absolute_url(self):
        return reverse('reservations', args=[self.id])

    def __str__(self):
        return f'{self.author.first_name} {self.author.last_name}'
