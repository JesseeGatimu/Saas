from rest_framework.response import Response
from rest_framework import viewsets,status
from .serializers import ReviewSerializer
from .permissions import IsReviewerOrReadOnly
from .models import Review
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class ReviewViewSet(viewsets.ModelViewSet):
    queryset=Review.objects.select_related(
        "service",
        "reviewer",
    ).all()
    serializer_class=ReviewSerializer
    permission_classes=[
        IsAuthenticatedOrReadOnly,
        IsReviewerOrReadOnly,
    ]
    
    #instead of trusting the reviewer ID sent by the client let us assign the ID automatically
    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)