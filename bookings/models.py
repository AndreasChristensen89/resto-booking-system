from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.urls import reverse


STATUS = ((0, "Pending"), (1, "Approved"), (2, "Declined"))


class Table(models.Model):
    size = models.IntegerField()

    def __str__(self):
        return f'Table for {self.size}'


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
       
        if not self.booking_end and not self.slug and self.booking_start:
            self.booking_end = self.booking_start + timedelta(hours=3)
            self.slug = self.first_name+self.last_name
        super().save(*args, **kwargs)   

    class Meta:
        ordering = ["-created_on"]

    def get_absolute_url(self):
        return reverse('booking-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


WEEKDAYS = (
  (1, "Monday"),
  (2, "Tuesday"),
  (3, "Wednesday"),
  (4, "Thursday"),
  (5, "Friday"),
  (6, "Saturday"),
  (7, ("Sunday")),
)


class OpeningHours(models.Model):

    weekday = models.IntegerField(choices=WEEKDAYS)
    from_time = models.TimeField()
    to_time = models.TimeField()

    class Meta:
        ordering = ('weekday', 'from_time')
        unique_together = ('weekday', 'from_time', 'to_time')

    def __unicode__(self):
        return u'%s: %s - %s' % (self.get_weekday_display(),
                                 self.from_time, self.to_time)

    def __str__(self):
        return f'{self.weekday}: from {self.from_time} to {self.to_time}'
