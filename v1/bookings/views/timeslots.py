"""Views related to timeslots."""

from rest_framework import filters

from django.utils.translation import gettext_lazy as _

from base.views import IdDecodeModelViewSet


from v1.bookings import models as booking_models
from v1.bookings.serializers import timeslots as timeslot_serializers
from rest_framework import generics


class TimeSlotViewSet(IdDecodeModelViewSet):
    """
    View to list, create , update and delete TimeSlot data.
    """
    queryset = booking_models.TimeSlot.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = [filters.SearchFilter,]
    search_fields = ['name',]
    serializer_class = timeslot_serializers.TimeSlotSerializer


class AvailableTimeSlot(generics.CreateAPIView):
    """
    View to verify which claims can be inherited in a list of batches
    """

    serializer_class = timeslot_serializers.AvailableTimeSlotSerializer


class TimeSlotServiceViewSet(IdDecodeModelViewSet):
    """
    View to list, create , update and delete TimeSlot data.
    """
    queryset = booking_models.TimeSlotServices.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']
    # filter_backends = [filters.SearchFilter,]
    # search_fields = ['name',]
    serializer_class = timeslot_serializers.TimeSlotServiceSerializer
