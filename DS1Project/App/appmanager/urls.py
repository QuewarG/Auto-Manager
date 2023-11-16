from django.urls import path, include
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('adminpage/', adminpage, name='adminpage'),
    path('sucursales/', sucursales, name='sucursales'),
    path('users/', users, name='users'),
    path('users/signup/', signup, name='signup'),
    path('users/edit_user/', edit_usuario, name='edit_usuario'),
    path('users/delete_user/', delete_Usuario, name='delete_user'),
    path('roles/', roles, name='roles'),
    path('roles/create_rol/', create_rol, name='new_rol'),
    path('roles/edit_rol/', edit_rol, name='edit_rol'),
    path('roles/delete_rol/', delete_rol, name='delete_rol'),
    path('inventory/', inventory, name='inventory'),
    path('orders/', orders, name='orders'),
    path('cotizaciones/', cotizaciones, name='cotizaciones'),
    path('sales/', sales, name='sales'),
    path('reports/', reports, name='reports'),
    path('logout/', exit, name='exit'),
]
