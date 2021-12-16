from django.contrib import admin
from .models import Booking, Table


@admin.register(Booking)
class AdminBookings(admin.ModelAdmin):

    list_display = ('booking_start', 'number_guests', 'status', 'author', )
    search_fields = ['booking_start', 'status']
    list_filter = ('status', 'booking_start')
    actions = ['pending', 'approve', 'decline']

    def pending(self, request, queryset):
        queryset.update(status=0)

    def approve(self, request, queryset):
        queryset.update(status=1)

    def decline(self, request, queryset):
        queryset.update(status=2)


@admin.register(Table)
class AdminTable(admin.ModelAdmin):

    list_display = ('seats', 'zone', 'table_number', 'moveable')
    search_fields = ['zone', 'seats', 'table_number', 'moveable']
    list_filter = ('seats', 'zone', 'table_number', 'moveable')
