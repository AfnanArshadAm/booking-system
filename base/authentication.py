import jwt
from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication

from utilities.functions import decode
from base.session import set_to_local
from rest_framework import permissions

from v1.accounts.models import CustomUser, ValidationToken

from . import exceptions as base_exec


class CustomAuthentication(JWTAuthentication):
    """
    Authentication class customized to set session data to thread local storage
    """

    def authenticate(self, request):
        """
        Call the default authentication mechanism to validate the token and
        fetch the user.
        Then, additional session data received in the token is set to
        thread local storage
        """
        user_token = super(
            CustomAuthentication, self).authenticate(request)
        if not user_token:
            return None
        user, validated_token = user_token

        session_data = {
            k: decode(v) if k.endswith('_id') else v
            for k, v in validated_token['session_data'].items()
        }
        for k, v in session_data.items():
            set_to_local(k, v)
        return user, validated_token


class IsTokenAuthenticated(permissions.BasePermission):
    """
    Check if the user is authenticated.

    Authentication to check if the user access token is valid
    and fetch the user from the token and add it to kwargs.
    """

    def has_permission(self, request, view):
        """Function to check token."""
        key = request.META.get('HTTP_AUTHORIZATION')
        if not key:
            raise base_exec.AccessForbidden(
                'Can not find Bearer token in the request header.')
        key = str.replace(str(key), 'Bearer ', '')
        data = jwt.decode(
            key, key=settings.SECRET_KEY,
            algorithms=['HS256'], options={'verify_exp': False})
        try:
            user = CustomUser.objects.get(
                id=decode(data['session_data'].get('user_id')))
        except:
            raise base_exec.AccessForbidden('User not found')
        session_data = {
            k: decode(v) if k.endswith('_id') else v
            for k, v in data['session_data'].items()
        }
        for k, v in session_data.items():
            set_to_local(k, v)
        if user.is_blocked:
            raise base_exec.AccessForbidden(
                'user account is blocked, contact admin.')
        request.user = user
        view.kwargs['user'] = user
        view.kwargs['data'] = data
        return True


# class ValidTotp(permissions.BasePermission):
#     """Check if the given totp and language is valid."""

#     def has_permission(self, request, view):
#         """Function to check token."""
#         if settings.ENVIRONMENT == 'local':
#             return True
#         current_otp = request.META.get('HTTP_OTP')
#         if not current_otp:
#             raise base_exec.BadRequest(
#                 'Can not find OTP in the request header.')
#         totp = pyotp.TOTP(settings.TOTP_TOKEN)

#         if totp.verify(current_otp, valid_window=1):
#             return True
#         raise base_exec.AccessForbidden("Invalid otp")


class IsTokenValidation(permissions.BasePermission):
    """
    Check if the user is authenticated.

    Authentication to check if the user access token is valid
    and fetch the user from the token and add it to kwargs.
    """

    def has_permission(self, request, view):
        """Function to check token."""
        key = request.META.get('HTTP_TOKEN')
        salt = request.META.get('HTTP_SALT')
        if not key:
            raise base_exec.BadRequest(
                'Can not find token in the request header.')
        if not salt:
            raise base_exec.BadRequest(
                'Can not find salt in the request header.')
        try:
            token = ValidationToken.objects.get(
                key=key, id=decode(salt))
            view.kwargs['notification'] = token.notification
            view.kwargs['token'] = token
        except:
            raise base_exec.BadRequest('User not found')
        return True
