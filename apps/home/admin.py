# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin



from apps.home.models import ServiceRequest,Equipo,ServiceResponse,Software,ComputoRegistrado,Area# Register your models here.
admin.site.register(ServiceRequest)
admin.site.register(Equipo)
admin.site.register(Software)
admin.site.register(ServiceResponse)
admin.site.register(ComputoRegistrado)
admin.site.register(Area)

