
from django.urls import path
from . import views

urlpatterns = [
    path('', views.busFinder, name='findBus'),
    path('search/result/<int:id1>/<int:id2>/', views.result, name='result'),
]
