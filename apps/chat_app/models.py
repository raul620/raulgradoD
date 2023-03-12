from django.db import models
from datetime import datetime
from apps.home.models import ServiceRequest

# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=1000)
    ServiceRequest = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE,null=True)

class Message(models.Model):
    value = models.CharField(max_length=1000000)
    date = models.DateTimeField(default=datetime.now, blank=True)
    user = models.CharField(max_length=1000000)
    room = models.CharField(max_length=1000000)