from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import StockViewset

app_name = "employee"

router = DefaultRouter()
router.register("", StockViewset)


urlpatterns = [
    path('', include(router.urls)),
]
