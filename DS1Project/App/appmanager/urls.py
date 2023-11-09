from django.urls import path, include
from .views import adminpage, exit, users, roles

urlpatterns = [
    path('', adminpage, name='adminpage'),
    path('users/', users, name='users'),
    path('roles/', roles, name='roles'),
    path('logout/', exit, name='exit'),
]
