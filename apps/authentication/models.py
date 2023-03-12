# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_pic = models.ImageField(null= True,upload_to='static/media/pfp')
    city= models.CharField(max_length=30, blank=True)
    country= models.CharField(max_length=30, blank=True)
    postal_code= models.CharField(max_length=30, blank=True)
    phone_number= models.CharField(max_length=30, blank=True)
    
    