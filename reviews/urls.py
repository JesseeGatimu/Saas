from django.urls import path,include
from .views import ReviewViewSet
from rest_framework.routers import DefaultRouter

router=DefaultRouter()

router.register("reviews",ReviewViewSet,basename="review")

urlpatterns = [
    path("",include(router.urls)),
]
