from django.urls import path
from . import views

urlpatterns = [  
    path('loginPage/',views.loginPage,name="login_page"),
    path('logout/',views.logoutuser,name="logout_page"),

    path('',views.home,name="home"),
    path('room/<str:pk>/',views.room,name="room" ),
    path('createRoom/',views.createRoom,name="create_room"),
     path('AddTopic/',views.AddTopic, name="add_topic"),
    path('UpdateRoom/<str:pk>/',views.UpdateRoom,name="update_room"),
    path('delete/<str:pk>/,',views.delete,name="delete"),
    path('UpdateTopic/<str:pk>/',views.UpdateTopic,name="update_topic"),
    path('register/',views.registerPage,name="register")

]