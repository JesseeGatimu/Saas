from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=Review
        fields=["id","service","reviewer","rating","comment","created_at","updated_at"]
        read_only_fields=["id","reviewer","created_at","updated_at"]
        
    def validate(self,attrs):
        service=attrs.get(
            "service",
            getattr(self.instance,"service",None),
        )
        request=self.context.get("request")
        
        if request and request.user.is_authenticated and service:
            if service.owner_id==request.user.pk:
                raise serializers.ValidationError(" You cannot review your own service. ")
            existing_reviews=Review.objects.filter(
                service=service,
                reviewer=request.user,
            )
            
            if self.instance:
                exoisting_reviews=existing_reviews.exclude(
                    pk=self.instance.pk
                )
            if existing_reviews.exists():
                raise serializers.ValidationError(
                    "You already have a review for this service"
                )
        return attrs