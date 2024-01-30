
from django.urls import path
from . import views

app_name = 'stands'
urlpatterns = [
    path('standlist/', views.stands, name='stands'),
    path('standlist/<int:stand_id>/', views.stand, name='stand'),
    path('new_stand/', views.new_stand, name='new_stand'),
    path('edit_stand/<int:stand_id>/', views.edit_stand, name='edit_stand'),
    path('new_area/', views.new_area, name='new_area'),
    
    # path('add_stand_for_stand/<int:bus_id>/', views.add_stand_for_bus, name='add_stand_for_bus'),
    # path('edit/<int:bus_id>/<int:order>/', views.edit_bus_stand, name='edit_bus_stand'),
    # path('delete/<int:bus_id>/<int:order>/', views.delete_bus_stand, name='delete_bus_stand'),
]
