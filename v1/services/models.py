from django.db import models
from django.contrib.postgres.fields import ArrayField

from django.utils.translation import gettext_lazy as _

from common.library import _get_file_path

from base.models import AbstractBaseModel


class Category(AbstractBaseModel):
    """
    Model to store categories of the providers.

    Attribs:
        name(char)      : Category name.
    """

    name = models.CharField(max_length=500, default="",
                            null=True, blank=True, verbose_name=_("Category Name"))

    def __str__(self):
        """Object name in django admin."""
        return f"{self.name}"


class ServiceProvider(AbstractBaseModel):
    """
    Model to store Service providers.

    Attribs:
        name(char)           : Name of the service provider.
        category(obj)        : Category of a service provider.
        description(str)     : Description about the service provider.
        experience(str)      : Eexperience about the service provider.
        description(str)     : description about the service provider.
        opening_time(time)   : Provider start time per day.
        closing_time(time)   : Provider end time per day.
        break_time(duration) : Provider break duration per day.
        holidays(str)        : Holidays of this service provider in a week.
        all_services(str)    : List of services provided by this provider.

    Inherited Attribs:
        creator(obj): Creator user of the object.
        updater(obj): Updater of the object.
        created_on(datetime): Added date of the object.
        updated_on(datetime): Last updated date of the object.
    """

    name = models.CharField(
        max_length=1000, default='', null=True, blank=True,
        verbose_name=_('Provider Name'))
    number = models.CharField(
        default='', max_length=200, null=True, blank=True,
        verbose_name=_('Provider Number'))
    email = models.EmailField(blank=True)
    profile_photo = models.ImageField(
        upload_to=_get_file_path, null=True, blank=True, verbose_name=_('profile photo'))
    category = models.ForeignKey(
        'services.Category', on_delete=models.SET_NULL,
        verbose_name=_('Provider Category'), related_name='category',
        null=True, blank=True)
    description = models.TextField(default='', null=True, blank=True)
    experience = models.TextField(default='', null=True, blank=True)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    break_time = models.DurationField()
    # holidays = models.TextField(default='', null=True, blank=True)
    holidays = ArrayField(models.CharField(
        max_length=200), null=True, blank=True)
    all_services = models.TextField(default='', null=True, blank=True)

    def __str__(self):
        """Function to return value in django admin."""
        return f'{self.name} - {self.idencode}'

    # @classmethod
    # def initialize(cls):
    #     """
    #     Function to initialize the sync, ie first create a url and then
    #     request to core, in the response process the data and store it
    #     as a dictionary.
    #     """
    #     from v1.bookings.models import TimeSlot
    #     for provider in ServiceProvider.objects.all():
    #         print("sssss")
    #         # sync = Sync()
    #         # sync.response = sync.get_response()
    #         # sync.tenant = tenant
    #         # if sync.response:
    #         #     sync._records = sync.response['data']['records']
    #         #     if sync.response['data']['next']:
    #         #         sync._next = sync.response['data']['next']
    #         #         sync._records = sync.get_complete_data()
    #         # op_data_list = sync.get_data(tenant)
    #         # data = {
    #         #     'success': True,
    #         #     'status': sync.response['resultCode'],
    #         #     'records': sync._records
    #         # }
    #         # sync.response = data
    #         # sync.save()
    #     return True


class ProviderGallery(AbstractBaseModel):
    """
    Model to media files of Service providers.

    Attribs:
        title(char)       : Title for the media of provider.
        media(file)       : Media of service provider.
        provider(obj)     : Service provider of this media.

    Inherited Attribs:
        creator(obj): Creator user of the object.
        updater(obj): Updater of the object.
        created_on(datetime): Added date of the object.
        updated_on(datetime): Last updated date of the object.
    """

    title = models.CharField(
        max_length=1000, default='', null=True, blank=True,
        verbose_name=_('Provider image title'))
    media = models.FileField(
        upload_to=_get_file_path, null=False, blank=False, verbose_name=_('media'))
    provider = models.ForeignKey(
        ServiceProvider, on_delete=models.CASCADE,
        verbose_name=_('Provider images'), null=False, blank=False)

    def __str__(self):
        """Function to return value in django admin."""
        return f'{self.title} - {self.idencode}'

    @property
    def image_url(self):
        """Get file url ."""
        try:
            return self.image.url
        except:
            return None


class Service(AbstractBaseModel):
    """
    Model to store Service.

    Attribs:
        name(char)         : Name of the service provider.
        provider(obj)      : Service provider of this media.
        description(str)   : Description about the service provider.
        duration(duration) : Service duration.

    Inherited Attribs:
        creator(obj): Creator user of the object.
        updater(obj): Updater of the object.
        created_on(datetime): Added date of the object.
        updated_on(datetime): Last updated date of the object.
    """

    title = models.CharField(
        max_length=1000, default='', null=True, blank=True,
        verbose_name=_('service title'))
    provider = models.ForeignKey(
        ServiceProvider, on_delete=models.CASCADE,
        verbose_name=_('Provider services'), null=False, blank=False)
    description = models.TextField(default='', null=True, blank=True)
    duration = models.DurationField()

    def __str__(self):
        """Function to return value in django admin."""
        return f'{self.title} - {self.idencode}'
