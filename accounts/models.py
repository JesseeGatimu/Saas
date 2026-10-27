from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLES=(
        ('admin','Admin'),
        ('trader','Trader'),
        ('client','Client')
    )
    role=models.CharField(max_length=20,choices=ROLES,default="client")
    email=models.EmailField(null=True,blank=True,unique=True)
    
    def __str__(self):
        return self.username
    



