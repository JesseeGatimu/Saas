from rest_framework import serializers
from .models import Services

class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Services
        Fields=[
            'id',
            'owner',
            'business_name',
            'service_name',
            'price_type',
            'price',
            'max_price',
            'description',
            'location',
            'created_at',
            'updated_at',
        ]
        read_only_fields=['id','owner','created_at','updated_at']