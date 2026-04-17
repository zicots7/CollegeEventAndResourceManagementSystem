"""
URL configuration for CollegeEventandResourceManagement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from Dashboards.views import dashboard_redirect
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('user.urls'),name='user'),
    path('dashboard/', dashboard_redirect, name='dashboard'),
    path('dashboard/',include('Dashboards.urls'),name='dashboard'),
    path('event/',include('event.urls'),name='event'),
    path('registration/', include('registration.urls'), name='registration'),
    path('resources/', include('resources.urls'), name='resources'),
    path('downloadResources/',include('downloadResources.urls'),name='downloadResources'),
    path('notifications/',include('notification.urls'),name='notifications'),
]
