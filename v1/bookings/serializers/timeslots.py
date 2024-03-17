"""serializers related to service provider."""

from rest_framework import serializers

from common.drf_custom import fields as custom_fields

from base import exceptions

from v1.services import models as service_models
from v1.services.serializers import provider as provider_serializers
from v1.bookings import models as booking_models
from v1.accounts import models as user_models

from datetime import datetime, timedelta
from django.utils.translation import gettext_lazy as _
from django.db.models import Q


class TimeSlotServiceSerializer(serializers.ModelSerializer):
    """Serializer for TimeSlot Services."""

    timeslot = custom_fields.IdencodeField(
        required=True, related_model=user_models.CustomUser)
    service = custom_fields.IdencodeField(
        required=True, related_model=service_models.ServiceProvider)

    class Meta:
        """Meta data."""
        model = booking_models.TimeSlotServices
        fields = (
            'idencode', 'timeslot', 'service'
        )


class ViewTimeSlotServiceSerializer(serializers.ModelSerializer):
    """Serializer to view TimeSlot Services."""

    service = provider_serializers.ServiceSerializer()

    class Meta:
        """Meta data."""
        model = booking_models.TimeSlotServices
        fields = (
            'idencode', 'service',
        )

# timeslotservicesx


class TimeSlotSerializer(serializers.ModelSerializer):
    """basic TimeSlot Serializer."""

    id = custom_fields.IdencodeField(read_only=True)
    customer = custom_fields.IdencodeField(
        required=True, related_model=user_models.CustomUser)
    provider = custom_fields.IdencodeField(
        required=True, related_model=service_models.ServiceProvider)
    timeslotservices = ViewTimeSlotServiceSerializer(read_only=True, many=True)

    class Meta:
        """Meta data."""
        model = booking_models.TimeSlot
        fields = (
            'id', 'date', 'provider', 'starting_time', 'ending_time', 'is_booked',
            'timeslotservices', 'customer', 'status', 'duration'
        )


class CreateTimeSlotSerializer(serializers.ModelSerializer):
    """Serializer for ServiceProvider."""

    id = custom_fields.IdencodeField(read_only=True)
    customer = custom_fields.IdencodeField(
        required=True, related_model=user_models.CustomUser)
    provider = custom_fields.IdencodeField(
        required=True, related_model=service_models.ServiceProvider)
    timeslotservices = custom_fields.ManyToManyIdencodeField(
        write_only=True, required=True, related_model=service_models.Service)

    class Meta:
        """Meta data."""
        model = booking_models.TimeSlot
        fields = (
            'id', 'date', 'provider', 'starting_time', 'ending_time', 'is_booked',
            'timeslotservices', 'customer', 'status', 'duration'
        )

    def validate(self, attrs):
        if booking_models.TimeSlot.objects.filter(
            Q(provider=attrs["provider"]) &
            Q(date=attrs["date"]) &
            (
                Q(starting_time=attrs["starting_time"]) |
                Q(ending_time=attrs["ending_time"])
            )
        ).exists():
            raise exceptions.Conflict(_("Time Slot already booked"))
        return attrs

    def create(self, validated_data):
        """
        Create overrided to add creator, updater and create
        user for this provider.
        """
        services = validated_data.pop('timeslotservices')
        validated_data["duration"] = sum(
            (service.duration for service in services), timedelta())
        timeslot = super().create(validated_data)
        for service in services:
            booking_models.TimeSlotServices.objects.create(
                timeslot=timeslot, service=service)
        return timeslot


class AvailableTimeSlotSerializer(serializers.Serializer):
    """
    Serializer to list available time slots.
    """
    provider = custom_fields.IdencodeField(
        write_only=True, required=True, related_model=service_models.ServiceProvider)
    services = custom_fields.ManyToManyIdencodeField(
        write_only=True, required=True, related_model=service_models.Service)

    class Meta:
        """Meta Info."""
        fields = ('provider', 'services',)

    def create(self, validated_data):
        services = validated_data['services']
        provider = validated_data['provider']

        total_duration = sum(
            (service.duration for service in services), timedelta())

        available_time_slots = []
        current_time = datetime.now()
        end_date = current_time + timedelta(days=7)

        while current_time <= end_date:
            if current_time.strftime('%a') in provider.holidays:
                current_time += timedelta(days=1)
                continue

            existing_time_slots = booking_models.TimeSlot.objects.filter(
                provider=provider, date=current_time.date())

            start_time = datetime.combine(
                current_time.date(), provider.opening_time)
            end_time = datetime.combine(
                current_time.date(), provider.closing_time)

            while start_time + total_duration <= end_time:
                if not existing_time_slots.filter(starting_time__lte=start_time.time(),
                                                  ending_time__gte=(start_time + total_duration).time()).exists():
                    available_time_slots.append({
                        'date': current_time.date(),
                        'starting_time': start_time.time(),
                        'ending_time': (start_time + total_duration).time(),
                    })
                start_time += timedelta(minutes=30)
            current_time += timedelta(days=1)

        return available_time_slots

    def to_representation(self, available_time_slots):
        """available timeslots returned."""
        return {'available_time_slots': available_time_slots}
