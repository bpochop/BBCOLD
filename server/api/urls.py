from django.urls import path
#Method 2 #from .views import home,settings,maintenance,menu,confirm,create
from .views import RoomView, CreateRoomView, JoinRoom, UserInRoom, pumpsView, menuView, Confirm

urlpatterns = [

    path('home', RoomView.as_view()),
    path('create-room', CreateRoomView.as_view()),
    path('join-room', JoinRoom.as_view()),
    path('user-in-room', UserInRoom.as_view()),
    path('get-pumps', pumpsView.as_view()),
    path ('get-menu', menuView.as_view()),
    path('confirm', Confirm.as_view())

    #method2
    # path('home', home),
    # path('settings', settings),
    # path('maintenance', maintenance),
    # path('menu', menu),
    # path('confirm', confirm),
    # path('create', create)

]

