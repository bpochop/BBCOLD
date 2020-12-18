from django.urls import path
#Method 2 #from .views import home,settings,maintenance,menu,confirm,create
from .views import RoomView, CreateRoomView

urlpatterns = [

    path('home', RoomView.as_view()),
    path('create-room', CreateRoomView.as_view())

    #method2
    # path('home', home),
    # path('settings', settings),
    # path('maintenance', maintenance),
    # path('menu', menu),
    # path('confirm', confirm),
    # path('create', create)

]
