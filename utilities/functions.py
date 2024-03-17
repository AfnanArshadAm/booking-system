"""
Utility functions used across apps
"""

import phonenumbers
import hashlib
import requests
from hashids import Hashids
from datetime import datetime

from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.functional import Promise


def encode(value):
    """
    Function to hash encode an integer value.

    Input Params:
        value(int): int value
    Returns:
        hashed string.
    """
    hasher = Hashids(
        min_length=settings.HASHID_MIN_LENGTH,
        alphabet=settings.HASHID_ALPHABETS,
    )
    try:
        value = int(value)
        return hasher.encode(value)
    except Exception as e:
        raise ValueError(
            _("Invalid input {value} for Encoder. Should be of type int").format(value=value))


def decode(value):
    """
    Function to hash decode an encoded value to int.

    Input Params:
        value(str): str value
    Returns:
        int value.
    """
    hasher = Hashids(
        min_length=settings.HASHID_MIN_LENGTH,
        alphabet=settings.HASHID_ALPHABETS,
    )
    try:
        return hasher.decode(value)[0]
    except Exception as e:
        raise ValueError(
            _("Invalid input({value}) for Decoder.").format(value=value))


def validate_phone(number):
    """
    Function to validate phone number.

    Input Params:
        number(str): international phone number
    Returns:
        dictionary with
        phone(str): phone number
        code(str): country code
    """
    try:
        number = number.replace(' ', '')
        number = number.replace('-', '')
        if not number.startswith('+'):
            number = '+' + number
        number = phonenumbers.parse(number)
        phone = str(number.national_number)
        code = '+' + str(number.country_code)
        return code + phone
    except Exception as e:
        print(e)
        return None


def hash_file(file):
    """
    Function to compute the hash of a file

    Args:
        file: file to be hashed.

    Returns:

    """
    if not file:
        return ''
    md5 = hashlib.md5()
    for chunk in file.chunks():
        md5.update(chunk)
    return md5.hexdigest()


def get_ip_from_request(request):
    """
    Function to get the IP address from the request.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')


def get_location_from_ip(ip):
    """
    Function to get the location data from the IP address.
    """
    location_data = requests.get(settings.IP_API_URL.format(ip=ip)).json()
    location_info = [location_data.get(
        i) for i in ['city', 'region', 'country_name'] if location_data.get(i, None)]
    return ', '.join(location_info)


def encode_list(id_list):
    """
    Function encodes list of ids.
    """
    return [encode(id) for id in id_list]


def decode_list(id_list):
    """
    Function decodes list of encoded ids.
    """
    return [decode(id) for id in id_list]
