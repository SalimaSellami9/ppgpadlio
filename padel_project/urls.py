"""
URL configuration for padel_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from . import views
from reservation_app import views

urlpatterns = [

    path('reservation/', views.rechercher_terrain, name='reservation'),
    path('reserver/', views.reserver, name='reserver'),
    path('admin/', admin.site.urls),
    path('', include('reservation_app.urls')),
    path('', views.home, name='home'), 
    path('terrains_list/', views.rechercher_terrain, name='terrains_list'),
    path('admin/', admin.site.urls),
    path('connecter/', views.connexion_view, name='connecter'),
    path('creerCompte/', views.creer_compte_view, name='creerCompte'),
]
