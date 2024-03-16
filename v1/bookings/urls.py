"""URLs of the app services."""

from rest_framework import routers
from django.urls import path

from v1.bookings.views import timeslots as timeslots_views

from v1.bookings import models as booking_models

router = routers.SimpleRouter()
urlpatterns = [
    path('available/', timeslots_views.AvailableTimeSlot.as_view()), ]

router.register(r'timeslots', timeslots_views.TimeSlotViewSet,
                basename=booking_models.TimeSlot)
router.register(r'timeslots', timeslots_views.TimeSlotServiceViewSet,
                basename=booking_models.TimeSlotServices)


urlpatterns += router.urls
