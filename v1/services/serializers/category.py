"""serializers related to category."""

from rest_framework import serializers

from common.drf_custom import fields as custom_fields

from v1.services import models as service_models


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for category."""

    id = custom_fields.IdencodeField(read_only=True)

    class Meta:
        """Meta data."""
        model = service_models.Category
        fields = ('id', 'name')
