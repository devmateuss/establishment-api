from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from user.views import UserViewSet
from establishment.views import EstabeblishmentsViewSet

router = routers.DefaultRouter()
router.register(r'user', UserViewSet)
router.register(r'establishment', EstabeblishmentsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
]
