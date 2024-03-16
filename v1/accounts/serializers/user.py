"""Serializers related to user are stored here."""
from rest_framework import serializers

from base import session
from common.drf_custom import fields as custom_fields
# from common.library import PhoneNumberField

from v1.accounts import models as user_models


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user."""

    id = custom_fields.IdencodeField(read_only=True)

    # default_node = custom_fields.IdencodeField(
    #     read_only=True, source='get_default_node')
    # node_name = serializers.SerializerMethodField(required=False)
    phone = custom_fields.PhoneNumberField(required=True)
    # button_data = serializers.SerializerMethodField(required=False)

    class Meta:
        """Meta info."""

        model = user_models.CustomUser
        fields = [
            'id', 'first_name', 'last_name', 'email', 'dob', 'phone',
            'address', 'image']

    # def get_node_name(self, obj):
    #     """Return the default node details."""
    #     return obj.node_name()

    # def get_button_data(self, obj):
    #     """Return the button data for frontend actions."""
    #     data = {
    #         'can_create_batch': False
    #     }
    #     if session.get_logged_node().admins.all().exists() and (
    #             session.get_logged_node() == session.get_current_node()):
    #         data['can_create_batch'] = True
    #     return data


class BasicUserSerializer(serializers.ModelSerializer):

    id = custom_fields.IdencodeField(read_only=True)

    class Meta:
        """Meta info."""

        model = user_models.CustomUser
        fields = [
            'id', 'first_name', 'last_name', 'email', 'image'
        ]
