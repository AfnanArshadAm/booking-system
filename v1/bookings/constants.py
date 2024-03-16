"""Constants under the user accounts section are stored here."""

from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeSlotStatus(models.IntegerChoices):
    PENDING = 101, _('Pending')
    ATTENDED = 111, _('Attended')
    CANCELED = 121, _('Canceled')
