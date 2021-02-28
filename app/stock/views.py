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
from .models import (Prediction, Like, Follow, Bookmark)
from .serializers import (PredictionSerializer, BookmarkSerializer, ListBookmarkSerializer,
                          BookmarkNoSerializer, LikeSerializer, FollowSerializer)
# Create your views here.


class PredictionViewset(viewsets.ModelViewSet):
    queryset = Prediction.objects.all()
    serializer_class = PredictionSerializer
    http_method_names = ['get']
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__firstname', 'user__lastname']
    ordering_fields = ['user__firstname', 'user__lastname', 'symbol']
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    
    def list(self, request, pk=None):
        try:
            page = request.GET.get('page', 1)
            response = requests.get(f'https://mboum.com/api/v1/co/collections/?list=day_gainers&start={page}&apikey={settings.STOCK_API_KEY}')
                
            return HttpResponse(response)
        
        except Exception as e:
            return Response({'success': False, 'errors': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
    
    def retrieve(self, request, pk=None):
        pass
    
    
    @action(methods=['GET'], detail=False, url_path='symbol/(?P<symbol>[^/.]+)')
    def get_stock(self, request, symbol, pk=None):
        try:
            
            response = requests.get(f'https://mboum.com/api/v1/hi/history/?symbol={symbol}&interval=1wk&diffandsplits=true&apikey={settings.STOCK_API_KEY}')

            return HttpResponse(response)
        
        except Exception as e:
            return Response({'success': False, 'errors': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
        
        

class BookmarkViewset(viewsets.ModelViewSet):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    http_method_names = ['get', 'post', 'delete']
    search_fields = ['user__firstname', 'prediction__symbol']
    filter_fields = ['user__firstname', 'prediction__symbol']
    ordering_fields = ['-created_at']
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    
    def get_serializer_class(self):
        if self.action in [ 'create', 'patch', 'retrieve']:
            return BookmarkSerializer
        
        elif self.action in ['list']:
            return ListBookmarkSerializer
        
        elif self.action in ['destroy']:
            return BookmarkNoSerializer
        
        return super().get_serializer_class()
    
    
    def get_permissions(self):
        permission_classes = self.permission_classes
        if self.action in ['retrieve', 'list','create', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
        
        

class LikeViewset(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    http_method_names = ['get', 'post', 'delete']
    search_fields = ['user__firstname', 'prediction__symbol']
    filter_fields = ['user__firstname', 'prediction__symbol']
    ordering_fields = ['-created_at']
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    
    def get_permissions(self):
        permission_classes = self.permission_classes
        if self.action in ['retrieve', 'list','create', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
        
        
class FollowViewset(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    http_method_names = ['get', 'post', 'delete']
    search_fields = ['follower__firstname', 'following__firstname']
    filter_fields = ['follower__firstname', 'following__firstname']
    ordering_fields = ['-created_at']
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    
    def get_permissions(self):
        permission_classes = self.permission_classes
        if self.action in ['retrieve', 'list','create', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)