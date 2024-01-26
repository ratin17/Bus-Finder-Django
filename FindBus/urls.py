
from django.urls import path
from . import views

urlpatterns = [
    path('', views.busFinder, name='findBus'),
    path('result/', views.result, name='result'),
]
