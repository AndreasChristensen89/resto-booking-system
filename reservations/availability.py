import datetime
from .models import Reservation, Table


def check_availability(date, time, time_end):
    availability_list = []
    reservations_list = Reservation.objects.filter(date=date)
    for reservation in reservations_list:
        if reservation.time > time_end or reservation.time_end < time:
            availability_list.append(True)
        else:
            availability_list.append(False)
    return all(availability_list)   # returns true if all is True
