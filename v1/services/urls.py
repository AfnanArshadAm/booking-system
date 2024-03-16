"""URLs of the app services."""

from rest_framework import routers
from django.urls import path

from v1.services.views import category as category_views
from v1.services.views import provider as provider_views
from v1.services import models as service_models

router = routers.SimpleRouter()
urlpatterns = []

router.register(r'categories', category_views.CategoryViewSet,
                basename=service_models.Category)
router.register(r'providers', provider_views.ServiceProviderViewSet,
                basename=service_models.ServiceProvider)
router.register(r'provider_images', provider_views.ProviderGalleryViewSet,
                basename=service_models.ProviderGallery)
router.register(r'services', provider_views.ServiceViewSet,
                basename=service_models.Service)

# urlpatterns = router.urls

urlpatterns += router.urls
