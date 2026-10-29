from django.conf import settings
from services.models import Services
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Review(models.Model):
    service=models.ForeignKey(Services,on_delete=models.CASCADE,related_name="reviews")
    reviewer=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="reviews")
    rating=models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1),MaxValueValidator(5)]
    )
    comment=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    class Meta:
        constraints=[
            models.UniqueConstraint(
                fields=["service","reviewer"],
                name="unique_review_per_user_per_service"
            )
        ]
        ordering=["-created_at"]
        
    def __str__(self):
        return (
            f"{self.reviewer} - {self.service}"
            f"{self.rating}/5"
        )