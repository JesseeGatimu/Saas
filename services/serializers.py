from rest_framework import serializers
from .models import Services, Profile, ServicePhoto

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