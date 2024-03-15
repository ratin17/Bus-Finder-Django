
from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.busFinder, name='findBus'),
    path('search/result/<int:id1>/<int:id2>/', views.result, name='result'),
    
    
    path('about/', views.about, name='about'),
    
    
    path('suggest-result/<int:dept_id>/<int:dest_id>/<int:bus_id>/<str:dist>/<str:busTime>/', views.suggestResult, name='suggest_result'),
    path('suggest-custom/', views.suggestCustom, name='suggest_custom'),
    path('suggest-bus/<int:bus_id>/', views.suggestBus, name='suggest_bus'),
    path('suggest-bus-stand/<int:bus_id>/<int:stand_id>/', views.suggestBusStand, name='suggest_bus_stand'),
    path('suggest-stand/<int:stand_id>/', views.suggestStand, name='suggest_stand'),
    path('suggest-area/<int:area_id>/', views.suggestArea, name='suggest_area'),
    
    
    path('feedback-custom/<str:msg>/', views.feedbackCustom, name='feedback_custom'),
    path('feedback-success/<str:msg>/<str:headline>/', views.feedbackSuccess, name='feedback_success'),
    path('feedback-error/<str:msg>/', views.feedbackError, name='feedback_error'),
    
]
