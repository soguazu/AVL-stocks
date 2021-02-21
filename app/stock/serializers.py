from rest_framework import serializers
from .models import (Stock,)
from datetime import datetime




class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'
        # extra_kwargs = {
        #     "employee": {'read_only': True},
        # }