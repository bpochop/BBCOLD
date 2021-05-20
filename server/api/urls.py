from django.urls import path
#Method 2 #from .views import home,settings,maintenance,menu,confirm,create
from .views import pumpsView, menuView, confirmView,SettingsView, CreateDrink, UpdatePumps

urlpatterns = [

    path('get-pumps', pumpsView.as_view()),
    path ('get-menu', menuView.as_view()),
    path('confirm', confirmView.as_view()),
    path('settings', SettingsView.as_view()),
    path('createDrink', CreateDrink.as_view()),
    path('updatePumps', UpdatePumps.as_view())

    #method2
    # path('home', home),
    # path('settings', settings),
    # path('maintenance', maintenance),
    # path('menu', menu),
    # path('confirm', confirm),
    # path('create', create)

]

