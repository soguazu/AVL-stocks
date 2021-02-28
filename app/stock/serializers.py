from rest_framework import serializers
from django.db import models
from .models import (Prediction, Like, Bookmark, Follow)
from datetime import datetime



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
        predictions = Prediction.objects.filter(id__in=models.Subquery(bookmarks.values('prediction__id')), bookmarked_book__user=self.context['request'].user)
        
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

        
class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'
        
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
    class Meta:
        model = Prediction
        fields = '__all__'
        
        extra_kwargs = {
                'deleted': {
                    'read_only': True
                }
            }
        