from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, User, AbstractUser, UserManager, \
    AbstractUser as DjangoAbstractUser
from django.utils.translation import gettext_lazy as _

from base.models import AbstractBaseModel
from base.models import CustomUserManager

from v1.accounts import constants as user_consts

from django.utils import timezone
import datetime


# class MyAccountManager(BaseUserManager):
#     def create_user(self, username, phone, password=None):
#         # if not email:
#         #     raise ValueError('Users must have an email address')
#         if not username:
#             raise ValueError('Users must have a username')

#         user = self.model(
#             # email=self.normalize_email(email),
#             username=username,
#             phone=phone,
#             password=password,
#         )

#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, username,phone, password):
#         user = self.create_user(
#             # email=self.normalize_email(email),
#             password=password,
#             phone=phone,
#             username=username,
#         )
#         user.is_admin = True
#         user.is_staff = True
#         user.is_superuser = True
#         user.role = 'admin'
#         user.save(using=self._db)

#         return user

# class CustomUser(AbstractBaseUser,AbstractBaseModel):

#     email = models.EmailField(verbose_name="email", max_length=60, null=True, blank=True)
#     username = models.CharField(max_length=15, unique=True)
#     date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
#     last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
#     is_admin = models.BooleanField(default=False,null=True,blank=True)
#     is_active = models.BooleanField(default=True,null=True,blank=True)
#     is_deleted = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False,null=True,blank=True)
#     is_superuser = models.BooleanField(default=False,null=True,blank=True)
#     full_name = models.TextField(null=True,blank=True)
#     phone = models.CharField(max_length=10,null=False,blank=False, unique=True)
#     creator = models.CharField(max_length=60,null=True,blank=True)

#     dob = models.DateField(
#         null=True, blank=True, verbose_name=_('Date Of Birth'))
#     address = models.CharField(
#         default='', max_length=2000, null=True, blank=True,
#         verbose_name=_('Address'))
#     image = models.URLField(
#         null=True, default=None, blank=True, verbose_name=_('Photo'))
#     status = models.IntegerField(
#         default=user_consts.UserStatus.CREATED,
#         choices=user_consts.UserStatus.choices, verbose_name=_('User Status'))
#     is_blocked = models.BooleanField(
#         default=False, verbose_name=_('Block User'))


#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = ['phone']

#     objects = BaseUserManager()

#     def __str__(self):
#         return self.username

#     def has_perm(self,perm,obj=None):
#         return self.is_admin

#     def has_module_perms(self,app_label):
#         return True


# class CustomUser(AbstractBaseUser,AbstractBaseModel):
class CustomUser(DjangoAbstractUser, AbstractBaseModel):

    """
    Base User model.

    Attribs:
        dob(date): Date of birth of user.
        phone (str): phone number of the user.
        address(str): address of the user.
        language(int): Language preference.
        image (img): user image.
        type (int): Type of the user like
            admin ,provider, staff or user etc.
        status(int): Current status of the user like created or active.
        blocked(bool): field which shows the active status of user.

    Inherited Attribs:
        username(char): Username for the user for login.
        email(email): Email of the user.
        password(char): Password of the user.
        first_name(char): First name of the user.
        last_name(char): Last name of the user.
        date_joined(date): User added date.

    """
    dob = models.DateField(
        null=True, blank=True, verbose_name=_('Date Of Birth'))
    phone = models.CharField(
        default='', max_length=200, null=True, blank=True,
        verbose_name=_('Phone Number'))
    address = models.CharField(
        default='', max_length=2000, null=True, blank=True,
        verbose_name=_('Address'))
    image = models.URLField(
        null=True, default=None, blank=True, verbose_name=_('Photo'))
    type = models.IntegerField(
        default=user_consts.UserType.USER,
        choices=user_consts.UserType.choices, verbose_name=_('User Type'))
    status = models.IntegerField(
        default=user_consts.UserStatus.CREATED,
        choices=user_consts.UserStatus.choices, verbose_name=_('User Status'))
    is_blocked = models.BooleanField(
        default=False, verbose_name=_('Block User'))
    # provider = models.ForeignKey(
    #     'services.Provider', null=True, on_delete=models.SET_NULL,
    #     blank=True, verbose_name=_("Provider"), related_name='providers')

    # objects = UserManager()
    objects = CustomUserManager()

    class Meta:
        """Meta class for the above model."""

        verbose_name = ('Base User')

    def __str__(self):
        """Object name in django admin."""
        return self.first_name

    def save(self, *args, **kwargs):
        if not self.username and self.email:
            self.username = self.email
        return super(CustomUser, self).save(*args, **kwargs)

    @property
    def image_url(self):
        """Get file url ."""
        try:
            return self.image.url
        except:
            return None

    @property
    def name(self):
        """Get user full name."""
        return f'{self.get_full_name()}'

    def set_active(self):
        self.status = user_consts.UserStatus.ACTIVE
        self.save()

    # # @property
    # # def policy_accepted(self):
    # #     """
    # #     Return privacy info related to the user.
    # #     """
    # #     if self.accepted_policy == PrivacyPolicy.current_privacy_policy():
    # #        return True
    # #     return False

    # def make_force_logout(self):
    #     """Method makes force logout true"""
    #     self.force_logout = True
    #     self.save()
    #     return True

    # def disable_force_logout(self):
    #     """Method to make force logout false."""
    #     self.force_logout = False
    #     self.save()
    #     return True


class ValidationToken(AbstractBaseModel):
    """
    Class to store the validation token data.

    This is a generic model to store and validate all
    sort of tokens including password setters, one time
    passwords and email validations..

    Attribs:
        user(obj): user object
        key (str): token.
        status(int): status of the validation token
        expiry(datetime): time up to which link is valid.
        type(int): type indicating the event associated.

    Inherited Attribs:
        creator(obj): Creator user of the object.
        updater(obj): Updater of the object.
        created_on(datetime): Added date of the object.
        updated_on(datetime): Last updated date of the object.
    """

    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        related_name='validation_tokens', verbose_name=_('Token User'),
        null=True, blank=True)

    ip = models.CharField(default='', max_length=500, blank=True)
    location = models.CharField(default='', max_length=500, blank=True)
    device = models.CharField(default='', max_length=500, blank=True)

    key = models.CharField(max_length=200, verbose_name=_('Token'))
    status = models.IntegerField(
        default=user_consts.ValidationTokenStatus.UNUSED,
        choices=user_consts.ValidationTokenStatus.choices,
        verbose_name=_('Token Status'))
    expiry = models.DateTimeField(
        default=timezone.now, verbose_name=_('Token Expiry Date'))
    type = models.IntegerField(
        default=user_consts.ValidationTokenType.VERIFY_EMAIL,
        choices=user_consts.ValidationTokenType.choices,
        verbose_name=_('Token Type'))

    def __str__(self):
        """Object name in django admin."""
        return f'{self.user.name} : {self.key} :  {self.id}'

    def save(self, *args, **kwargs):
        """
        Overriding the default save signal.

        This function will generate the token key based on the
        type of the token and save when the save() function
        is called if the key is empty. It. will. also set the
        expiry when the object is created for the first time.
        """
        if not self.key:
            self.key = self.generate_unique_key()
        if not self.id:
            self.expiry = self.get_expiry()
        return super(ValidationToken, self).save(*args, **kwargs)

    @property
    def creation_time_str(self):
        return pendulum.instance(self.created_on).format(
            "hh:mm A on dddd, DD-MM-YYYY")

    def get_validity_period(self):
        return user_consts.TOKEN_VALIDITY[self.type]

    def get_expiry(self):
        """Function to get the validity based on type."""
        validity = self.get_validity_period()
        return (timezone.now() + datetime.timedelta(
            minutes=validity))

    def generate_unique_key(self):
        """Function to generate unique key."""
        if self.type != user_consts.ValidationTokenType.OTP:
            key = get_random_string(settings.ACCESS_TOKEN_LENGTH)
        else:
            key = common_lib._generate_random_number(settings.OTP_LENGTH)

        if ValidationToken.objects.filter(
                key=key, type=self.type,
                status=user_consts.ValidationTokenStatus.UNUSED).exists():
            key = self.generate_unique_key()
        return key

    def validate(self):
        """Function to. validate the token."""
        status = True
        if not self.is_valid:
            status = False
        self.status = user_consts.ValidationTokenStatus.USED
        self.updater = self.user
        self.save()
        return status

    def refresh(self):
        """Function  to refresh the validation token."""
        if not self.is_valid:
            self.key = self.generate_unique_key()
            self.status = user_consts.ValidationTokenStatus.UNUSED
        self.expiry = self.get_expiry()
        self.updater = self.user
        self.save()
        return True

    def mark_as_used(self):
        """ Function to mark validation token as used """
        self.status = user_consts.ValidationTokenStatus.USED
        self.save()

    @staticmethod
    def initialize(user, type, ip="", location="", device=""):
        """Function to initialize verification."""
        token = ValidationToken.objects.create(
            user=user, status=user_consts.ValidationTokenStatus.UNUSED,
            type=type)
        token.ip = ip
        token.location = location
        token.device = device
        token.save()
        return token

    @property
    def validity(self):
        """Function to get the validity of token."""
        return common_lib._date_time_desc(self.expiry)

    @property
    def created_on_desc(self):
        """Function to get the validity of token."""
        return common_lib._date_time_desc(self.created_on)

    def is_valid(self):
        """Function  which check if Validator is valid."""
        if self.expiry > timezone.now() and (
                self.status == user_consts.ValidationTokenStatus.UNUSED):
            return True
        return False

    def invalidate(self):
        """
        Function chnage the status of the token into used and change the 
        expiry date of the token.
        """
        self.mark_as_used()
        self.expiry = timezone.now()
        self.save()
        return True

    def get_expires_in(self):
        """
        Return token expiry pending days.
        """
        pending_days = 0
        if self.expiry < timezone.now():
            self.mark_as_used()
            return pending_days
        pending_days = (self.expiry - timezone.now()).days
        return pending_days


class AccessToken(models.Model):
    """
    The default authorization token model.

    This model is overriding the DRF token
    Attribs:
        user(obj): user object
        Key(str): token
        created(datetime): created date and time.
        device(obj): device object
    """

    user = models.ForeignKey(
        CustomUser, related_name='authe_token',
        on_delete=models.CASCADE, verbose_name=_('Token User'),
        null=True, blank=True)
    key = models.CharField(
        max_length=200, unique=True, verbose_name=_('Token'))
    created = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Created Date'))

    def __str__(self):
        """Function to return value in django admin."""
        return self.key

    def save(self, *args, **kwargs):
        """Overriding the save method to generate key."""
        if not self.key:
            self.key = self.generate_unique_key()
        return super(AccessToken, self).save(*args, **kwargs)

    def generate_unique_key(self):
        """Function to generate unique key."""
        key = get_random_string(settings.ACCESS_TOKEN_LENGTH)
        if AccessToken.objects.filter(key=key).exists():
            self.generate_unique_key()
        return key

    def refresh(self):
        """Function  to change token."""
        self.key = self.generate_unique_key()
        self.save()
        return self.key
