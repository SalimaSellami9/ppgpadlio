from django.urls import path
from . import views


urlpatterns = [
    path('reserver/', views.reserver, name='reserver'),
    path('terrains_list/', views.rechercher_terrain, name='terrains_list'),
]



