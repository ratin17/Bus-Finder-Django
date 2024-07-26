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
    path('suggestions/all/', views.allSuggestions, name='all-suggestions'),
    path('read/suggestions/read/', views.readSuggestions, name='read-suggestions'),
    path('suggestions/unread/', views.unreadSuggestions, name='unread-suggestions'),
    
    path('suggestion/delete/<int:id>/', views.deleteSuggestion, name='delete-suggestion'),
    path('suggestion/read/<int:id>/', views.readSuggestion, name='read-suggestion'),
    
    
    
    
    path('logs/', views.logs, name='logs'),
    path('logs/all/', views.allLogs, name='all-logs'),
    path('logs/type/<str:type>/', views.typeLogs, name='type-logs'),
    
    path('logs/delete/past/<int:n>/<str:choice>/', views.keepLogsOfLast_X_DaysOrHoursOrMinutes, name='keep-last-logs'),
    path('logs/delete/last/<int:n>/<str:choice>/', views.deleteLogsOfLast_X_DaysOrHoursOrMinutes, name='delete-last-logs'),
    path('logs/delete/old/<int:n>/', views.keepLatest_X_Logs, name='keep-last-n-logs'),
    path('logs/delete/type/<str:type>/', views.deleteLogsOfType_X, name='delete-logs-type'),
    path('logs/delete/all/', views.deleteAll, name='delete-all-logs'),
    
]