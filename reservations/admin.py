from django.contrib import admin
from .models import Reservations

# Register your models here.
@admin.register(Reservations)
class AdminReservations(admin.ModelAdmin):

    list_display = ('first_name', 'last_name', 'status', 'created_on')
    search_fields = ['first_name', 'last_name', 'date']
    list_filter = ('status', 'created_on')
    actions = ['pending', 'approve', 'decline']
    prepopulated_fields = {'slug': ('first_name', 'last_name',)}

    def pending(self, request, queryset):
        queryset.update(status=0)

    def approve(self, request, queryset):
        queryset.update(status=1)

    def decline(self, request, queryset):
        queryset.update(status=2)
