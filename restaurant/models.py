from django.db import models
import calendar


WEEKDAYS = (
  (0, "Monday"),
  (1, "Tuesday"),
  (2, "Wednesday"),
  (3, "Thursday"),
  (4, "Friday"),
  (5, "Saturday"),
  (6, ("Sunday")),
)


class OpeningHours(models.Model):
    weekday = models.IntegerField(choices=WEEKDAYS)
    from_time = models.TimeField()
    to_time = models.TimeField()

    class Meta:
        ordering = ('weekday', 'from_time')
        unique_together = ('weekday', 'from_time', 'to_time')
        verbose_name = 'Opening hours'
        verbose_name_plural = 'Opening hours'

    def __unicode__(self):
        return u'%s: %s - %s' % (self.get_weekday_display(),
                                 self.from_time, self.to_time)

    def __str__(self):
        list(calendar.day_abbr)
        ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        return f'{calendar.day_name[self.weekday]}: {self.from_time} to {self.to_time}'


class BookingDetails(models.Model):
    booking_duration = models.PositiveIntegerField()
    auto_table_assign = models.BooleanField()

    class Meta:
        verbose_name = 'Booking detail'
        verbose_name_plural = 'Booking details'

    def __str__(self):
        return f'{self.booking_duration} min bookings - auto table-assignment: {self.auto_table_assign}'
