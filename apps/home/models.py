# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from psycopg2 import Timestamp
#from requests import post
from apps.authentication.models import User
from django.db.models.signals import post_save
from taggit.managers import TaggableManager
# Create your models here.
import datetime
class Area(models.Model):
	nombre=models.CharField(max_length=200, null=True,blank=True, default='no registrado')
	def __str__(self):
		return self.nombre
class ComputoRegistrado(models.Model):
	Area = models.ForeignKey('Area', on_delete=models.RESTRICT,null=True,blank=True)
	modelo = models.CharField(max_length=200, null=True,blank=True)
	caracteristicas = models.CharField(max_length=200, null=True,blank=True)
	ip_dir = models.CharField(max_length=200, null=True,blank=True, default=None)
	mac_dir = models.CharField(max_length=200, null=True,blank=True, default=None)
	date_registed = models.DateTimeField(auto_now=True, null=True)
	def __str__(self):
    
		return self.modelo
class ServiceRequest(models.Model):

	Area = models.ForeignKey('Area', on_delete=models.RESTRICT,null=True,blank=True)
	ComputoRegistrado= models.ForeignKey('ComputoRegistrado', on_delete=models.RESTRICT,null=True,blank=True)
	
	STATUS = [
			('Pending', 'Pending'),
			('Taken by staff', 'Taken by staff'),
			('Solved', 'Solved'),
	]
	title = models.CharField(max_length=200, null=True,blank=True)

	customer = models.ForeignKey(User,related_name='related_customerl_user', on_delete=models.CASCADE, default=1 )
	ip_dir = models.CharField(max_length=200, null=True,blank=True, default=None)
	mac_dir = models.CharField(max_length=200, null=True,blank=True, default=None)
	takenby = models.ForeignKey(User,related_name='related_takenby_user' ,on_delete=models.CASCADE, default=None,blank=True, null=True)
	
	date_created = models.DateTimeField(default=datetime.datetime.now, null=True)
	status = models.CharField(max_length=200, null=True, choices=STATUS, default='Pending',blank=True)
 
	description = models.CharField(max_length=200, null=True,blank=True )

	screenshot = models.ImageField(null=True,blank=True,upload_to='static/media/screenshot', default=None)
	tags = TaggableManager(blank=True)
	habilited = models.BooleanField(default=True)


	def __str__(self):
		return str(self.title)
class Equipo(models.Model):
	ServiceRequest = models.ForeignKey('ServiceRequest', on_delete=models.CASCADE)
	nombre_equipo= models.CharField(max_length=200, null=True,blank=True )
	modelo= models.CharField(max_length=200, null=True,blank=True)
	descripcion= models.CharField(max_length=200, null=True,blank=True)
 
	def __str__(self):
		return str(self.nombre_equipo)
class ServiceResponse(models.Model):
	ServiceRequest = models.ForeignKey('ServiceRequest', on_delete=models.CASCADE)
	description = models.CharField(max_length=200, null=True,blank=True )

	screenshot = models.ImageField(null=True,blank=True,upload_to='static/media/screenshot', default=None)

	def __str__(self):
		return str(self.description)
class Software(models.Model):
	ServiceRequest = models.ForeignKey(
        'ServiceRequest', on_delete=models.CASCADE
        )
	nombre_software= models.CharField(max_length=200, null=True,blank=True )
	descripcion= models.CharField(max_length=200, null=True,blank=True)
 
	def __str__(self):
		return self.ServiceRequest.title



'''

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

new_group, created = Group.objects.get_or_create(name='myTech')
new_group, created = Group.objects.get_or_create(name='myUser')

#permission = Permission.objects.create()
#new_group.permissions.add(permission)
'''