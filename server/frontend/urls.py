from django.urls import path
from .views import index

app_name = 'frontend'

urlpatterns = [
    path('', index),
    path('menu', index),
    path('settings',index),
    path('create', index),
    path('menu/confirm', index),
    path('survey', index),
    path('maintenance', index),
    
]
