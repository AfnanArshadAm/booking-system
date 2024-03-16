from django.db import models

from django.utils.translation import gettext_lazy as _

from common.library import _get_file_path

from base.models import AbstractBaseModel

from v1.services import models as service_models
from v1.accounts import models as user_models
from v1.bookings import constants as booking_consts


class TimeSlot(AbstractBaseModel):
    """
    Model to store Service providers.

    Attribs:
        provider(obj)       : Provider of a Timeslot.
        date(sate)          : Date of Timeslot.
        starting_time(time) : Timeslot start time.
        ending_time(time)   : Timeslot end time.
        is_booked(bool)     : Is this Timslot booked or not.

    Inherited Attribs:
        creator(obj): Creator user of the object.
        updater(obj): Updater of the object.
        created_on(datetime): Added date of the object.
        updated_on(datetime): Last updated date of the object.
    """
    customer = models.ForeignKey(
        user_models.CustomUser, on_delete=models.CASCADE, related_name='customer',
        verbose_name=_('Customer'), null=False, blank=False)
    provider = models.ForeignKey(
        service_models.ServiceProvider, on_delete=models.CASCADE,
        verbose_name=_('Provider services'), null=False, blank=False)
    date = models.DateField(
        null=True, blank=True, verbose_name=_('Date Of Time Slot'))
    starting_time = models.TimeField()
    ending_time = models.TimeField()
    is_booked = models.BooleanField(default=False)
    duration = models.DurationField(null=True, blank=True)
    status = models.IntegerField(
        default=booking_consts.TimeSlotStatus.PENDING,
        choices=booking_consts.TimeSlotStatus.choices, verbose_name=_('Time Slot Status'))

    def __str__(self):
        """Function to return value in django admin."""
        return f'{self.id} - {self.idencode}'


class TimeSlotServices(AbstractBaseModel):
    """
    Model to store Service providers.

    Attribs:
        provider(obj)       : Provider of a Timeslot.
        date(sate)          : Date of Timeslot.
        starting_time(time) : Timeslot start time.
        ending_time(time)   : Timeslot end time.
        is_booked(bool)     : Is this Timslot booked or not.

    Inherited Attribs:
        creator(obj): Creator user of the object.
        updater(obj): Updater of the object.
        created_on(datetime): Added date of the object.
        updated_on(datetime): Last updated date of the object.
    """
    timeslot = models.ForeignKey(
        TimeSlot, on_delete=models.CASCADE, related_name='timeslot',
        verbose_name=_('Timeslot'), null=False, blank=False)
    service = models.ForeignKey(
        service_models.Service, on_delete=models.CASCADE,
        verbose_name=_('timeslot services'), null=False, blank=False)

    def __str__(self):
        """Function to return value in django admin."""
        return f'{self.id} - {self.idencode}'
