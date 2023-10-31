from django.urls import path, include
from .views import home, adminpage, exit

urlpatterns = [
    path('', home, name='home'),
    path('adminpage/', adminpage, name='adminpage'),
    path('logout/', exit, name='exit'),
]
