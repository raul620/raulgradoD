# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.urls import path, include  # add this
from django.conf.urls.static import static
from django.conf import settings
import notifications.urls
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),          # Django admin route
    path("", include("apps.authentication.urls")), # Auth routes - login / register

    # ADD NEW Routes HERE
    path("chat/", include("apps.chat_app.urls")),
    path('inbox/notifications/', include(notifications.urls, namespace='notifications')),
    
    
    
    
    #reset
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), name ='reset-password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name ='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name ='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name ='password_reset_complete'),




    # Leave `Home.Urls` as last the last line
    path("", include("apps.home.urls")),
  
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)