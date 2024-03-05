
from django.urls import path
from . import views

urlpatterns = [
    path('', views.busFinder, name='findBus'),
    path('search/result/<int:id1>/<int:id2>/', views.result, name='result'),
    
    
    path('suggest/bus/<int:bus_id>/', views.suggest_bus, name='suggest_bus'),
    path('suggest/bus/stand/<int:bus_id>/<int:stand_id>/', views.suggest_bus_stand, name='suggest_bus_stand'),
    
    
    path('sugesstions/<int:switch>/<int:p1>/<int:p2>/<int:p3>/<int:p4>/', views.create_suggestion, name='create_suggestion'),
    
    
    path('success/<str:msg>/<str:suggest>/suggestion/', views.feedback, name='feedback'),
    
]
