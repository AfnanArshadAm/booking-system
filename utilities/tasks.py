# """
# Celery tasks
# """
# from v1.notifications import models as noti_models
# from v1.notifications.email_apis import EmailApi
# from common import constants as comm_consts
# import logging
# import sentry_sdk
# from sentry_sdk import capture_exception
# from celery import shared_task
# from django.utils import timezone
# import datetime

# from django.conf import settings
# from django.core.mail import send_mail

# from django.utils.html import strip_tags

# logger = logging.getLogger(__name__)


# @shared_task(name='sync_data')
# def create_timeslot():
#     """Function to sync_data"""
#     from v1.bookings import models as booking_models

#     sentry_sdk.capture_message(f'Timeslot creation started')
#     sync, op_data_list = Sync.initialize()
#     Node.initialize(data_list=op_data_list, sync=sync)
#     sentry_sdk.capture_message(f'Timeslot creation completed')
#     return True
