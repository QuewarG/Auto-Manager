from django.urls import path, include
from .views import *

urlpatterns = [
    path('', adminpage, name='adminpage'),
    path('users/', users, name='users'),
    path('users/signup/', signup, name='signup'),
    path('users/edit_user/', edit_usuario, name='edit_usuario'),
    path('users/delete_user/', delete_Usuario, name='delete_user'),
    path('roles/', roles, name='roles'),
    path('logout/', exit, name='exit'),
]
