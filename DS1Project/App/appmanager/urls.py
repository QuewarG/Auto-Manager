from django.urls import path, include
from .views import adminpage, exit, users, roles, signup

urlpatterns = [
    path('', adminpage, name='adminpage'),
    path('users/', users, name='users'),
    path('signup/', signup, name='signup'),
    path('roles/', roles, name='roles'),
    path('logout/', exit, name='exit'),
]
