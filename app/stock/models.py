from django.db import models
import uuid
from datetime import datetime, timedelta, timezone
from django.conf import settings
from django.contrib.postgres.fields import ArrayField



PREDICTION_OPTIONS = (
    ('BUY', 'BUY'),
    ('SELL', 'SELL'),
)

LIKE_STATUS = (
    ('PENDING', 'PENDING'),
    ('LIKE', 'LIKE'),
    ('UNLIKE', 'UNLIKE'),
)


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True  # Set this model as Abstract
    
    


class Prediction(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="client")
    last_price = models.FloatField(blank=True, null=True)
    symbol = models.CharField(max_length=25)
    remarks = models.TextField()
    prediction = models.CharField(max_length=25, choices=PREDICTION_OPTIONS)
 

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return str(self.user)
    
    
    
class Like(BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_liked")
    prediction = models.ForeignKey(Prediction, on_delete=models.CASCADE, related_name="liked_prediction")
    status = models.CharField(max_length=25, choices=LIKE_STATUS, default='PENDING')


    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return str(self.user)
    
    
class Follow(BaseModel):
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_follower")
    following = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_following")

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return str(self.following)
    
    

class Bookmark(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_bookmarks")
    prediction = models.ForeignKey(Prediction, on_delete=models.CASCADE, related_name="bookmark_prediction")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return str(self.user)


