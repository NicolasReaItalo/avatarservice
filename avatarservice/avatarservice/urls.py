"""
URL configuration for avatarservice project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from avatar.views import  get_avatar_list, get_image , upload_image

urlpatterns = [
    path('upload/', upload_image, name='upload_image'),
    path('avatar/<uuid:img_id>/', get_image, name='get_image'),
    path('avatar_list/', get_avatar_list, name='get_image'),
]