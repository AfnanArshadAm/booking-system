# """Celery configurations are specified here."""

# from __future__ import absolute_import, unicode_literals
# import os
# from celery import Celery

# os.environ.setdefault(
#     'DJANGO_SETTINGS_MODULE', 'booking_system.settings.base')

# app = Celery('booking_system')

# app.config_from_object('django.conf:settings', namespace='CELERY')
# app.conf.timezone = 'UTC'
# app.autodiscover_tasks()
