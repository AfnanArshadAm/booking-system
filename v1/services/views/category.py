"""Views related to category."""

from rest_framework import filters

from django.utils.translation import gettext_lazy as _

from base.views import IdDecodeModelViewSet
from base import session

from base.response import SuccessResponse

from v1.services import models as service_models
from v1.services.serializers import category as category_serializers


class CategoryViewSet(IdDecodeModelViewSet):
    """
    View to list, create , update and delete category data.
    """
    queryset = service_models.Category.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = [filters.SearchFilter,]
    search_fields = ['name',]
    serializer_class = category_serializers.CategorySerializer
