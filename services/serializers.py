from rest_framework import serializers
from .models import Services, Profile, ServicePhoto

class ServicesSerializer(serializers.ModelSerializer):
    average_rating=serializers.FloatField(read_only=True,allow_null=True)
    review_count=serializers.IntegerField(read_only=True)
    class Meta:
        model=Services
        fields=[
            'id',
            'owner',
            'business_name',
            'service_name',
            'price_type',
            'price',
            'max_price',
            'description',
            'average_rating',
            'review_count',
            'location',
            'created_at',
            'updated_at',
        ]
        read_only_fields=['id','owner','average_rating','review_count','created_at','updated_at']
        
        
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields=['id','user','profile_picture']
        read_only_fields=['id','user']
        
class ServicePhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model=ServicePhoto
        fields=['id','service','image','caption','created_at']
        read_only_fields=['id','created_at']