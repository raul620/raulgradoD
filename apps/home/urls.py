# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from . import views
from .views import (
    ProductList, ProductCreate, ProductUpdate,
    delete_image, delete_variant
)

urlpatterns = [

    # The home page
    path('', views.index, name='home'),

    #path('create', views.create, name='create'),
    path('search_results', views.SearchResultsView, name='search_results'),
    path('search_results_tables/', views.SearchResultsViewTable,
         name='search_results_tables'),
    path('view_tables', views.viewTables, name='view_tables'),
    path('view_order/<str:pk>', views.viewOrder, name="view_order"),
    path('statistics', views.statistics, name="statistics"),
    path('iniciar_chat/<str:pk>/', views.iniciarChat, name='iniciar_chat'),
    path('read_notification/<str:pk>/',
         views.readNotifications, name='read_notification'),
    path('generar_reporte/<str:pk>', views.generarReporte, name='generar_reporte'),

    #path('create_hardware', views.createHardware, name='create_hardware'),
    path('get_notifications', views.getNotifications, name='get_notifications'),
    path('notifcations', views.notifcations, name='notifcations'),
       path('eliminate_order/<str:pk>/', views.eliminateOrder, name='eliminate_order'),
    #     path('update_order/<str:pk>/', views.updateOrder, name='update_order'),

    #path('edit_hardware/<str:pk>', views.editHardware, name='edit_hardware'),
    #path('delete_hardware/<str:pk>', views.deleteHardware, name='delete_hardware'),

    path('create/',views.ProductCreate.as_view(), name='create'),
    path('update/<int:pk>/', views.ProductUpdate.as_view(), name='update_order'),

    path('delete-variant/<int:pk>/', views.delete_variant, name='delete_variant'),
    path('delete-image/<int:pk>/', views.delete_image, name='delete_image'),
    


   path('create_area/', views.create_area, name='create_area'),
      path('create_equipo/', views.create_equipo, name='create_equipo'),

    #path('products/', ProductList.as_view(), name='list_products'),

   path('select1/', views.select1, name='select1'),
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),


]
