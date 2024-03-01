from django.contrib import admin
from django.urls import path,include
from.import views

app_name = 'manage'
urlpatterns = [
    path('', views.manage, name='manage'),
    path('configure/', views.configure, name='configure'),
    path('remove/', views.removeData, name='remove'),
    path('addAreas/', views.addAreas, name='addAreas'),
    path('addStands/', views.addStands, name='addStands'),
    path('addBuses/', views.addBuses, name='addBuses'),
    path('addBusStands/', views.addBusStands, name='addBusStands'),
]