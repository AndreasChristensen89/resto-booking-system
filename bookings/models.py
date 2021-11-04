from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta


STATUS = ((0, "Pending"), (1, "Approved"), (2, "Declined"))


class Table(models.Model):
    size = models.PositiveIntegerField()

    def __str__(self):
        return f'Table with capacity for {self.size} people'


class Booking(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='table_booking')
    number_guests = models.PositiveIntegerField()
    booking_start = models.DateTimeField()
    booking_end = models.DateTimeField(blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    comment = models.TextField(max_length=300)
    table = models.ManyToManyField(Table, related_name='booking_tables', blank=True)
    
    def save(self, *args, **kwargs):
        if not self.booking_end and self.booking_start:
            self.booking_end = self.booking_start + timedelta(hours=3)
            super().save(*args, **kwargs)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
