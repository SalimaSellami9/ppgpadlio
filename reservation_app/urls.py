from django.urls import path
from . import views


urlpatterns = [
    path('reservation/', views.reserver, name='reservation'),
    path('terrains_list/', views.terrains_list, name='terrains_list'),
]



