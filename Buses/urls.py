
from django.urls import path
from . import views

urlpatterns = [
    path('buslist/', views.buses, name='buses'),
    path('buslist/<int:bus_id>/', views.bus, name='bus'),
    path('editBus/<int:bus_id>/', views.edit_bus, name='edit_bus'),
    path('new_bus/', views.new_bus, name='new_bus'),
    path('add_stand_for_bus/<int:bus_id>/', views.add_stand_for_bus, name='add_stand_for_bus'),
    path('edit/<int:bus_id>/<int:order>/', views.edit_bus_stand, name='edit_bus_stand'),
    path('delete/<int:bus_id>/<int:order>/', views.delete_bus_stand, name='delete_bus_stand'),
    
    
]
