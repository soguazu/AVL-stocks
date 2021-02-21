from django.db import models
import uuid
from datetime import datetime, timedelta, timezone
from django.conf import settings
from django.contrib.postgres.fields import ArrayField




class Stock(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f"{self.id}"


