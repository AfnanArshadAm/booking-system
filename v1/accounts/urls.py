# from django.urls import path
# from rest_framework import routers
# from .views import *
# from . import views


# app_name = 'v1.accounts'

# router = routers.DefaultRouter()
# # router.register('user',views.AccountViewSet, basename='user')


# urlpatterns=[

#     # path('login/', login_view, name="login"),
#     # path('logout/', logout_view, name="logout"),
# ]


# urlpatterns += router.urls





"""URLs of the app accounts."""

from rest_framework import routers

from django.urls import path

from v1.accounts.views import user as user_viewset

from v1.accounts import models as user_models


router = routers.SimpleRouter()

router.register(r'users', user_viewset.UserViewSet, 
    basename=user_models.CustomUser)

urlpatterns = router.urls

urlpatterns += []
