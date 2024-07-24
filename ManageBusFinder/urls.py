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
    
    
    path('suggestions/', views.suggestions, name='suggestions'),
    path('all/suggestions/', views.allSuggestions, name='all-suggestions'),
    path('read/suggestions/', views.readSuggestions, name='read-suggestions'),
    path('unread/suggestions/', views.unreadSuggestions, name='unread-suggestions'),
    
    path('suggestion/delete/<int:id>/', views.deleteSuggestion, name='delete-suggestion'),
    path('suggestion/read/<int:id>/', views.readSuggestion, name='read-suggestion'),
    
    
]