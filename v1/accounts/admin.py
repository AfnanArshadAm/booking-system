# from django.contrib import admin
# from .models import *


# class AccountAdmin(admin.ModelAdmin):
#     list_display = ('id','email','username','is_active','full_name','phone')
# admin.site.register(Account,AccountAdmin)


"""Models are registered with django admin at here."""

from django.contrib import admin
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin


from v1.accounts import models as user_models


# deployment = settings.DEPLOYMENT.capitalize()
# admin.site.site_header = _('%s C-Sink Registry Admin' % deployment)
# admin.site.site_title = _('C-Sink Registry: %s Admin Portal' % (deployment))
# admin.site.index_title = _('Welcome to C-Sink Registry %s Portal' % (
#     deployment))


class ValidationTokenAdmin(admin.ModelAdmin):
    """Class view to customize validation token admin."""

    ordering = ('-updated_on',)

    def salt(self, obj):
        """Get salt."""
        return obj.idencode

    list_display = (
        'user', 'key', 'status', 'salt', 'type', 'expiry'
    )
    list_filter = ('type', 'status')


class AccessTokenAdmin(admin.ModelAdmin):
    """Class view to customize validation token admin."""

    def email(self, obj):
        """ Show email in list"""
        return obj.user.email

    list_display = (
        'user', 'email', 'key'
    )


class AccessTokenInline(admin.TabularInline):
    """In-line view function for SourceBatch."""

    def get_user_id(self, obj):
        return obj.user.idencode

    readonly_fields = ('get_user_id', 'key', 'created')
    model = user_models.AccessToken
    extra = 0
    can_delete = False
    show_change_link = False

    def has_add_permission(self, request, obj=None):
        return False


class CustomUserAdmin(UserAdmin):
    """ Overriding user adminto add additional fields"""
    # readonly_fields = ('idencode', 'default_node')
    ordering = ('-id',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {
            'fields': ('first_name', 'last_name', 'email',
                       'dob', 'phone', 'address', 'image')
        }),
        (_('Internal values'), {
            'fields': ('type', 'status'),
        }),

        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = (
        'id', 'idencode', 'first_name', 'last_name', 'email',
    )


admin.site.register(user_models.CustomUser, CustomUserAdmin)
admin.site.register(user_models.AccessToken, AccessTokenAdmin)
admin.site.register(user_models.ValidationToken, ValidationTokenAdmin)
