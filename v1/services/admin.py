"""Models are registered with django admin at here."""

from django.contrib import admin

from common.admin import BaseAdmin

from v1.services import models as services_models


class CategoryAdmin(BaseAdmin):
    list_display = ("id", "name", "idencode",)
    search_fields = ["name"]


class ServiceProviderAdmin(BaseAdmin):
    list_display = ("id", "name", "idencode",
                    "number", "email", "profile_photo")
    search_fields = ["name"]


class ProviderGalleryAdmin(BaseAdmin):
    list_display = ("id", "title", "idencode", "media", "provider")
    search_fields = ["title"]


class ServiceAdmin(BaseAdmin):
    list_display = ("id", "title", "idencode",
                    "provider", "description", "duration")
    search_fields = ["title"]


admin.site.register(services_models.Category, CategoryAdmin)
admin.site.register(services_models.ServiceProvider, ServiceProviderAdmin)
admin.site.register(services_models.ProviderGallery, ProviderGalleryAdmin)
admin.site.register(services_models.Service, ServiceAdmin)
