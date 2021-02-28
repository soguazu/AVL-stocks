from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (PredictionViewset, BookmarkViewset, LikeViewset, FollowViewset)

app_name = "employee"

router = DefaultRouter()

router.register("follow", FollowViewset)
router.register("like", LikeViewset)
router.register("bookmark", BookmarkViewset)
router.register("", PredictionViewset)


urlpatterns = [
    path('', include(router.urls)),
]
