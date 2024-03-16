from .base import *

DEBUG = True

ALLOWED_HOSTS += [
    '0.0.0.0',
    'localhost',
    '127.0.0.1'
]

# INSTALLED_APPS += [
#     'drf_yasg',
# ]


SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'] = timedelta(days=14)
SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'] = timedelta(days=14)


# PYINSTRUMENT_PROFILE_DIR = 'profiles'
# ENABLE_PROFILING = False
# if ENABLE_PROFILING:
#     MIDDLEWARE += ['pyinstrument.middleware.ProfilerMiddleware']
