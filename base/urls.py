from django.urls import path
from .views import *


urlpatterns = [
    path('', home, name='home'),
    path('room/<int:id>', room, name='room'),
    path('create-room/', createRoom, name='create-room'),
    path('update-room/<int:id>', updateRoom, name='update-room'),
    path('delete-room/<int:id>', deleteRoom, name='delete-room'),
    path('delete-message/<int:id>', deleteMessage, name='delete-message'),
    path('login/', loginPage, name='login'),
    path('register/', registerPage, name='register'),
    path('logout/', logoutUser, name='logout'),
]