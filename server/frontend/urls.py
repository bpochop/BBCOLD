from django.urls import path
from .views import index
urlpatterns = [
    path('', index),
    path('menu', index),
    path('SettingsPage',index),
    path('create', index),
    path('menu/confirm', index),
    
]
