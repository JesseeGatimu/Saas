from django.shortcuts import get_object_or_404
from rest_framework import viewsets,status
from .serializers import ServicesSerializer, ServicePhotoSerializer, ProfileSerializer
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import MultiPartParser,FormParser
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, BasePermission
from rest_framework.views import APIView
from .permissions import IsOwnerOrReadOnly
from .models import Services, ServicePhoto, Profile
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db import models
from decimal import Decimal, InvalidOperation
from rest_framework.exceptions import ValidationError


class IsServicePhotoOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ["GET","HEAD","OPTIONS"]:
            return True
        return obj.service.owner==request.user
    
class ServiceViewSet(viewsets.ModelViewSet):
    queryset=Services.objects.all()
    serializer_class=ServicesSerializer
    permission_classes=[
        IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    ]
    filter_backends=[SearchFilter, OrderingFilter]
    search_fields=[
        "service_name",
        "business_name",
        "description",
        "location",
    ]
    
    ordering_fields=[
        "created_at",
        "updated_at",
        "price",
        "service_name",
    ]
    
    ordering=["-created_at"]
    
    def get_queryset(self):
        queryset=Services.objects.all()
        location=self.request.query_params.get("location")
        min_price=self.request.query_params.get("min_price")
        max_price=self.request.query_params.get("max_price")
        
        if location:
            queryset=queryset.filter(location_icontains=location)
            
        if min_price is not None:
            try:
                min_price=Decimal(min_price)
                if not min_price.is_finite() or min_price<0:
                    raise ValueError
            except(InvalidOperation, ValueError):
                raise ValidationError({
                    "min_price":"Enter a valid price"
                })
            
            queryset=queryset.filter(
                models.Q(price_gte=min_price),
                models.Q(max_price_gte=min_price)
            )
        
        if max_price is not None:
            try:
                max_price=Decimal(max_price)
                if not max_price.is_finite() or max_price<0:
                    raise ValueError
            except(InvalidOperation, ValueError):
                raise ValidationError({
                    "max_price":"Enter a valid price"
                })
                
            queryset=queryset.filter(price_lte=max_price)
            
        if (min_price is not None and max_price is not None and min_price>max_price):
            raise ValidationError({
                "price":"Min price cannot be greater than max price"
            })
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        
class ServicePhotoViewSet(viewsets.ModelViewSet):
    queryset=ServicePhoto.objects.select_related("service","service_owner").all()
    serializer_class=ServicePhotoSerializer
    permission_classes=[
        IsServicePhotoOwnerOrReadOnly,
        IsAuthenticatedOrReadOnly,
    ]
    parser_classes=[MultiPartParser,FormParser]
    
    def perform_create(self, serializer):
        service=serializer.validated_data["service"]
        
        if service.owner!=self.request.user:
            raise PermissionDenied("You can only upload photos to your own services. !")
        serializer.save()
        
    
class MyProfileView(APIView):
    permission_classes=[IsAuthenticated]
    parser_classes=[MultiPartParser,FormParser]
    
    def get_profile(self):
        profile,created=Profile.objects.get_or_create(user=self.request.user)
        return profile
    
    def get(self,request):
        profile=self.get_profile()
        serializer=ProfileSerializer(profile,context={"request":request},)
        return Response(serializer.data)
    
    def patch(self,request):
        profile=self.get_profile()
        serializer=ProfileSerializer(
            profile,data=request.data,partial=True,context={"request":request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)
    