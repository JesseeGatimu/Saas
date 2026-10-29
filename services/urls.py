from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ServiceViewSet, ServicePhotoViewSet, MyProfileView

router=DefaultRouter()
router.register("services",ServiceViewSet,basename="service")
router.register("service-photos",ServicePhotoViewSet,basename="service-photos")

urlpatterns = [
    path("",include(router.urls)),
    path("profile/me/",MyProfileView.as_view(),name="my-profile"),
]
