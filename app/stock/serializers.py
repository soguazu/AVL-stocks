from rest_framework import serializers
from django.conf import settings
from django.db import models
import requests
from .models import (Prediction, Like, Bookmark, Follow)
from datetime import datetime
from user.models import User


class ListUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'firstname', 'lastname', 'email', 'roles',
                  'image', 'verified', 'last_login', 'created_at',
                  'twitter', 'facebook', 'instagram']


class BookmarkNoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = []
        
        extra_kwargs = {
                'deleted': {
                    'read_only': True
                }
            }



class ListBookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = '__all__'
        
        extra_kwargs = {
            'deleted': {
                'read_only': True
            }
        }
    



class BookmarkSerializer(serializers.ModelSerializer):
    predictions = serializers.SerializerMethodField('get_predictions', read_only=True)
    class Meta:
        model = Bookmark
        fields = '__all__'
        
        extra_kwargs = {
                'deleted': {
                    'read_only': True
                },
                'user': {
                    'read_only': True
                }
            }
        
    
    def get_predictions(self, obj):
        bookmarks = Bookmark.objects.all()
        predictions = Prediction.objects.filter(id__in=models.Subquery(bookmarks.values('prediction__id')), user_bookmarks=self.context['request'].user)
        
        if predictions is None:
            return None
           
        serializer = PredictionSerializer(predictions, many=True)
        return serializer.data
    


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'
        
        extra_kwargs = {
                'deleted': {
                    'read_only': True
                }
            }



class FollowNoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = []
        
        extra_kwargs = {
                'deleted': {
                    'read_only': True
                }
            }


        
class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'
        
        extra_kwargs = {
                'deleted': {
                    'read_only': True
                },
                'follower': {
                    'read_only': True
                }
            }
        
        

class PredictionNoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        fields = []
        
        extra_kwargs = {
                'deleted': {
                    'read_only': True
                }
            }



        
class ListPredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        fields = '__all__'
        
        extra_kwargs = {
                'deleted': {
                    'read_only': True
                }
            }


class PredictionSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField('get_profile', read_only=True)
    amount_made = serializers.SerializerMethodField('get_amount_made', read_only=True)
    class Meta:
        model = Prediction
        exclude = ('user',)
        
        extra_kwargs = {
                'deleted': {
                    'read_only': True
                },
            }
        
        
    def get_profile(self, obj):
        user = User.objects.filter(id=obj.user.id).first()
        if user is not None:
            serializer = ListUserSerializer(user)
            return serializer.data
        return None
    
    
  
    
    def get_amount_made(self, obj):
        prediction = Prediction.objects.filter(id=obj.id).first()
        if prediction is None:
            return None
        
        new_prediction = requests.get(f'https://mboum.com/api/v1/hi/history/?symbol={prediction.symbol}&interval=1wk&diffandsplits=true&apikey={settings.STOCK_API_KEY}')
        data = new_prediction.json()
        
        response = ((data['meta']['regularMarketPrice'] - prediction.last_price) / prediction.last_price) * 100
        return response
        