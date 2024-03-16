"""serializers related to service provider."""

from rest_framework import serializers

from common.drf_custom import fields as custom_fields

from base import session

from v1.services import models as service_models
from v1.bookings import models as booking_models
from v1.accounts import models as user_models

from datetime import datetime, timedelta


class TimeSlotServiceSerializer(serializers.ModelSerializer):
    """Serializer for ServiceProvider."""

    # id = custom_fields.IdencodeField(read_only=True)
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


# timeslotservices


class TimeSlotSerializer(serializers.ModelSerializer):
    """Serializer for ServiceProvider."""

    id = custom_fields.IdencodeField(read_only=True)
    customer = custom_fields.IdencodeField(
        required=True, related_model=user_models.CustomUser)
    provider = custom_fields.IdencodeField(
        required=True, related_model=service_models.ServiceProvider)
    timeslot = TimeSlotServiceSerializer(read_only=True, many=True)
    aaasd = custom_fields.ManyToManyIdencodeField(
        write_only=True, required=True, related_model=service_models.Service)

    class Meta:
        """Meta data."""
        model = booking_models.TimeSlot
        fields = (
            'id', 'date', 'provider', 'starting_time', 'ending_time', 'is_booked',
            'aaasd', 'customer', 'status', 'duration', 'timeslot'
        )

    def create(self, validated_data):
        """
        Create overrided to add creator, updater and create
        user for this provider.
        """
        services = validated_data.pop('aaasd')
        total_duration = sum(
            (service.duration for service in services), timedelta())
        validated_data["duration"] = total_duration
        timeslot = super().create(validated_data)
        for service in services:
            booking_models.TimeSlotServices.objects.create(
                timeslot=timeslot, service=service)
        return timeslot


# class TimeSlotSerializer(serializers.ModelSerializer):
#     """Serializer for ServiceProvider."""

#     id = custom_fields.IdencodeField(read_only=True)
#     customer = custom_fields.IdencodeField(
#         required=True, related_model=user_models.CustomUser)
#     provider = custom_fields.IdencodeField(
#         required=True, related_model=service_models.ServiceProvider)
#     services = TimeSlotServiceSerializer(read_only=True, many=True)
#     timeslotservices = custom_fields.ManyToManyIdencodeField(
#         write_only=True, required=True, related_model=service_models.Service)

#     class Meta:
#         """Meta data."""
#         model = booking_models.TimeSlot
#         fields = (
#             'id', 'date', 'provider', 'starting_time', 'ending_time', 'is_booked',
#             'timeslotservices', 'customer', 'status', 'duration', 'services'
#         )

#     def create(self, validated_data):
#         """
#         Create overridden to add creator, updater and create
#         user for this provider.
#         """
#         services_data = validated_data.pop('timeslotservices', [])
#         total_duration = timedelta()  # Initialize total duration
#         for service_id in services_data:
#             # Extract the id from the service object
#             service_id = service_id.id if isinstance(
#                 service_id, service_models.Service) else service_id
#             service = service_models.Service.objects.get(id=service_id)
#             total_duration += service.duration

#         validated_data['duration'] = total_duration

#         timeslot = super().create(validated_data)

#         # Create TimeSlotServices instances
#         for service_id in services_data:
#             booking_models.TimeSlotServices.objects.create(
#                 timeslot=timeslot, service_id=service_id.id)

#         return timeslot


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

        # Calculate the total duration of all selected services
        total_duration = sum(
            (service.duration for service in services), timedelta())

        available_time_slots = []
        current_time = datetime.now()
        end_date = current_time + timedelta(days=7)

        # Iterate through each date in the next 7 days
        while current_time <= end_date:
            # Check if the current day is a holiday for the provider
            if current_time.strftime('%a') in provider.holidays:
                current_time += timedelta(days=1)
                continue

            # Get all existing time slots for the current date and provider
            existing_time_slots = booking_models.TimeSlot.objects.filter(
                provider=provider, date=current_time.date())

            # Calculate the start and end time for each time slot based on provider's opening and closing hours
            start_time = datetime.combine(
                current_time.date(), provider.opening_time)
            end_time = datetime.combine(
                current_time.date(), provider.closing_time)

            # Iterate through time slots for the current date
            while start_time + total_duration <= end_time:
                # Check if the time slot is available (not already booked)
                if not existing_time_slots.filter(starting_time__lte=start_time.time(),
                                                  ending_time__gte=(start_time + total_duration).time()).exists():
                    # Add the available time slot to the list
                    available_time_slots.append({
                        'date': current_time.date(),
                        'starting_time': start_time.time(),
                        'ending_time': (start_time + total_duration).time(),
                    })
                # Move to the next time slot
                # Adjust based on the required interval
                start_time += timedelta(minutes=30)

            # Move to the next day
            current_time += timedelta(days=1)

        return available_time_slots

    def to_representation(self, available_time_slots):
        """Inheritable claims returned."""
        return {'available_time_slots': available_time_slots}
