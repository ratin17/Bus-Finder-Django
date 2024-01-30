from django.contrib import admin
from django.urls import path,include
from.import views

app_name = 'manage'
urlpatterns = [
    path('', views.manage, name='manage'),
    path('configure/', views.configure, name='configure'),
]