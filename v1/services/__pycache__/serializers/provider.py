"""serializers related to service provider."""

from rest_framework import serializers

from common.drf_custom import fields as custom_fields

from base import session

from v1.services import models as service_models
from v1.accounts.serializers import user as accountserializer
from v1.accounts import models as user_models
from v1.accounts import constants as user_consts


class ServiceProviderSerializer(serializers.ModelSerializer):
    """Serializer for ServiceProvider."""

    id = custom_fields.IdencodeField(read_only=True)
    category = custom_fields.IdencodeField(
        required=False, related_model=service_models.Category)
    user = accountserializer.UserSerializer(
        required=True, write_only=True)

    class Meta:
        """Meta data."""
        model = service_models.ServiceProvider
        fields = (
            'id', 'name', 'number', 'email', 'profile_photo', 'category', 'description',
            'experience', 'opening_time', 'closing_time', 'break_time',
            'holidays', 'all_services', 'user'
        )

    def create_user(self, user):
        """Method to create user for this provider."""
        current_user = session.get_current_user()
        user = user_models.CustomUser.objects.create(
            type=user_consts.UserType.PROVIDER,
            creator=current_user, updater=current_user, **user
        )
        return user

    def create(self, validated_data):
        """
        Create overrided to add creator, updater and create
        user for this provider.
        """
        if 'user' in validated_data.keys():
            self.create_user(validated_data.pop('user'))
        return super().create(validated_data)


class ProviderGallerySerializer(serializers.ModelSerializer):
    """Serializer for ProviderGallery."""

    id = custom_fields.IdencodeField(read_only=True)
    provider = custom_fields.IdencodeField(
        required=True, related_model=service_models.ServiceProvider)

    class Meta:
        """Meta data."""
        model = service_models.ProviderGallery
        fields = ('id', 'title', 'media', 'provider')


class ServiceSerializer(serializers.ModelSerializer):
    """Serializer for Service."""

    id = custom_fields.IdencodeField(read_only=True)
    provider = custom_fields.IdencodeField(
        required=True, related_model=service_models.ServiceProvider)

    class Meta:
        """Meta data."""
        model = service_models.Service
        fields = ('id', 'title', 'provider', 'description', 'duration')
