"""Views related to category."""

from rest_framework import filters

from django.utils.translation import gettext_lazy as _

from base.views import IdDecodeModelViewSet
from base import session

from base.response import SuccessResponse

from v1.services import models as service_models
from v1.services.serializers import provider as provider_serializers


class ServiceProviderViewSet(IdDecodeModelViewSet):
    """
    View to list, create , update and delete provider data.
    """
    queryset = service_models.ServiceProvider.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = [filters.SearchFilter,]
    search_fields = ['name', 'phone', 'email']
    serializer_class = provider_serializers.ServiceProviderSerializer


class ProviderGalleryViewSet(IdDecodeModelViewSet):
    """
    View to list, create , update and delete provider data.
    """
    queryset = service_models.ProviderGallery.objects.all()
    http_method_names = ['get', 'post', 'delete']
    serializer_class = provider_serializers.ProviderGallerySerializer


class ServiceViewSet(IdDecodeModelViewSet):
    """
    View to list, create , update and delete serivce data.
    """
    queryset = service_models.Service.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = [filters.SearchFilter,]
    search_fields = ['title']
    serializer_class = provider_serializers.ServiceSerializer
