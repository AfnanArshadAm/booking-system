"""Models are registered with django admin at here."""

from django.contrib import admin

from common.admin import BaseAdmin

from v1.bookings import models as booking_models


class TimeSlotAdmin(BaseAdmin):
    list_display = ("idencode", "date", "starting_time",
                    "ending_time", "is_booked")
    search_fields = ["date"]


class TimeSlotServicesAdmin(BaseAdmin):
    list_display = ("idencode", "timeslot", "service")


admin.site.register(booking_models.TimeSlot, TimeSlotAdmin)
admin.site.register(booking_models.TimeSlotServices, TimeSlotServicesAdmin)
