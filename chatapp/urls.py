# chatapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/<str:room_name>/', views.dashboard, name='dashboard_with_room'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('chat/<str:room_name>/', views.chat_room, name='chat_room'),
    path('create-room/', views.create_room_view, name='create_room'),
    path('join-room/', views.join_room_view, name='join_room'),
    path('save-message/<str:room_name>/<str:username>/', views.save_message, name='save_message'),
    path('clear/<str:room_name>/', views.clear_chat, name='clear_chat'),
    path('send-pin-notification/', views.send_pin_notification, name='send_pin_notification'),
    path('blockchain/', views.blockchain_explorer, name='blockchain_explorer'),
    path('blockchain/tamper/<int:index>/', views.tamper_demo, name='tamper_demo'),

    path('upload/<str:room_name>/', views.upload_file, name='upload_file'),

    path('files/<str:room_name>/', views.list_files, name='list_files'),

    path('chat/<str:room_name>/', views.chat_room, name='chat_room1'),
]
