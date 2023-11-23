from django.urls import path, include
#from captcha import views as captcha_views
from .views import *

urlpatterns = [
    path('', home, name='home'),
    #path('captcha/', include('captcha.urls')),
    path('adminpage/', adminpage, name='adminpage'),
    path('cambiar_idioma/<str:idioma>/', cambiar_idioma, name='cambiar_idioma'),
    path('sucursales/', sucursales, name='sucursales'),
    path('sucursales/edit_sucursal', edit_sucursal, name='edit_sucursal'),
    path('sucursales/delete_sucursal', delete_Sucursal, name='delete_sucursal'),
    path('crear_sucursal/', create_sucursal, name='create_sucursal'),
    path('users/', users, name='users'),
    path('users/signup/', signup, name='signup'),
    path('users/edit_user/', edit_usuario, name='edit_usuario'),
    path('users/delete_user/', delete_Usuario, name='delete_user'),
    path('roles/', roles, name='roles'),
    path('roles/create_rol/', create_rol, name='new_rol'),
    path('roles/edit_rol/', edit_rol, name='edit_rol'),
    path('roles/delete_rol/', delete_rol, name='delete_rol'),
    path('inventory/', inventory, name='inventory'),
    path('inventory/create_product/', create_product, name='new_product'),
    path('inventory/edit_product/', delete_product, name='delete_product'), #edit_product
    path('inventory/delete_product/', delete_product, name='delete_product'), #delete_product
    path('orders/', orders, name='orders'),
    path('orders/cerrar_orden', cerrar_orden_trabajo, name='cerrar_orden_trabajo'),
    path('orders/create_order', create_order, name='create_order'),
    path('cotizaciones/', cotizaciones, name='cotizaciones'),
    path('cotizaciones/cambiar_estado_cotizacion', cambiar_estado_cotizacion, name='cambiar_estado_cotizacion'),
    path('cotizaciones/cotizar_reparacion', create_CotizacionReparacion, name='cotizacion_reparacion'),
    path('sales/', sales, name='sales'),
    path('consulta_reparacion/', consulta_reparacion_cliente, name='consulta_reparacion_cliente'),
    path('reports/', reports, name='reports'),
    path('logout/', exit, name='exit'),
    path('appmanager/login_user/', login_user, name='login'),
    path('i18n/', include('django.conf.urls.i18n')),
]
