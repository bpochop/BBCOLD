from django.contrib import admin
from django.urls import path
from .views import index
urlpatterns = [
    path('', index),
    path('menu', index),
    path('settings',index),
    path('create', index),
    path('menu/confirm', index),
    path('home', index),
    path('join', index),
    path('create', index),
    path('join/1', index),
    path('room/<str:roomCode>', index)
]
