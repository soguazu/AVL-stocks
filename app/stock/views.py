from django.shortcuts import render
from rest_framework import viewsets, permissions, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from sentry_sdk import capture_exception
from .models import (Stock,)
from .serializers import (StockSerializer, )
# Create your views here.


class StockViewset(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    # search_fields = ['user__firstname', 'user__lastname']
    # filter_fields = ['user__firstname']
    # ordering_fields = ['user__firstname', 'user__lastname']
    permission_classes = [IsAuthenticatedOrReadOnly]