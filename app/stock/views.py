from django.shortcuts import render
from rest_framework import viewsets, permissions, filters, status
import requests
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from django.http import HttpResponse
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import action
from sentry_sdk import capture_exception
from .models import (Stock,)
from .serializers import (StockSerializer, )
# Create your views here.


class StockViewset(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    http_method_names = ['get']
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    
    def list(self, request, pk=None):
        response = None
        if pk == None:
            response = requests.get(f'http://mboum.com/api/v1/co/collections/?list=day_gainers&start={page}&apikey={settings.STOCK_API_KEY}')
            
            
            
        # else:
        #     supplements =  models.Product.objects.filter(product_type=models.Product.SUPPLEMENT, id=pk)

        # supplements= self.filter_queryset(supplements)
        # page = self.paginate_queryset(response)
        return HttpResponse(response)