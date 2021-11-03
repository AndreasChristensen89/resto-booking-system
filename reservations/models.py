from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from datetime import timedelta


STATUS = ((0, "Pending"), (1, "Approved"), (2, "Declined"))


class Table(models.Model):
    size = models.PositiveIntegerField()

    class Meta:
        ordering = ["size"]

    def __str__(self):
        return f'Table with capacity of {self.size}'


class Reservation(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='table_reservations')
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    email = models.EmailField()
    phone = models.PositiveIntegerField()
    number_guests = models.PositiveIntegerField()
    date = models.DateField()
    time = models.TimeField()
    time_end = models.TimeField(blank=True, null=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    comment = models.TextField(max_length=300)

    def save(self):
        if not self.time_end and self.time:
            self.time_end = self.time
            self.time_end += timedelta(hours=3)
        super(Reservation, self).save()

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
