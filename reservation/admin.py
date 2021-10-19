from django.contrib import admin
from .models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):

    list_display = ('first_name', 'last_name', 'status', 'created_on')
    search_fields = ['first_name', 'last_name', 'date']
    list_filter = ('status', 'created_on')
    actions = ['pending', 'approve', 'decline']

    def pending(self, request, queryset):
        queryset.update(status=0)

    def approve(self, request, queryset):
        queryset.update(status=1)

    def decline(self, request, queryset):
        queryset.update(status=2)
