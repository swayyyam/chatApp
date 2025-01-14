from django.urls import path
from .views import *


urlpatterns = [
    path("chat/", chatPage, name="chat-page"),
    path('home/', homepage, name='homepage'),  
    path('', signup, name='signup'),  
    path('login/', login, name='login'), 
    path('logout/', logout_user, name='logout'),
    path('get_messages/<str:username>/', get_messages, name='get-messages'),
    path('delete_chat/<str:username>/', delete_chat, name='delete-messages'),

    
]