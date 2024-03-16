
from rest_framework import generics

from base.views import IdDecodeModelViewSet

import datetime

from v1.accounts import models as user_models
from v1.accounts.serializers import user as user_serializers
# from v1.apiauth import permissions as auth_permissions

from base import session


class UserViewSet(IdDecodeModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """

    queryset = user_models.CustomUser.objects.all()
    serializer_class = user_serializers.UserSerializer
    http_method_names = ['get', 'patch',]
