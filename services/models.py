from django.conf import settings
from django.db import models

class Services(models.Model):
    owner=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="services")
    business_name=models.CharField(max_length=200)
    service_name=models.CharField(max_length=200)
    price_type=models.CharField(
        max_length=20,
        choices=[
            ('fixed','Fixed'),
            ('range','Range'),
            ('starting','Starting'),
            ('negotiable','Negotiable'),
            ('dm','Dm for pricing'),
            ('free','Free'),
        ],
        default='fixed',
        )
    price=models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    max_price=models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    description=models.TextField()
    location=models.CharField(max_length=200, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.service_name