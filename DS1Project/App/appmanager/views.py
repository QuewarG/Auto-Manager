from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import *
from .forms import *
from django.db import IntegrityError
from django.utils.translation import gettext as _, activate
from django.conf import settings

# FUNCIONES DEL SISTEMA

def home(request):
    print (request.LANGUAGE_CODE)
    return render(request, "home.html")

@login_required
def adminpage(request):
    actual_user = request.user
    return render(request, 'adminpage.html', {'actual_user': actual_user})


def login_user(request):
    if request.method == 'GET':
        print (request.LANGUAGE_CODE)
        messages.get_messages(request)
        return render(request, 'registration/login.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('adminpage')

        else:
            msg =_('Ocurrió un error iniciando sesión. Intente nuevamente...')
            messages.success(request, msg)
            return redirect('login')

def exit(request):
    logout(request)
    return redirect('home')

#VISTAS DE PRUEBA
def roles(request):
    rol = Rol.objects.all()
    messages.get_messages(request)
    return render(request, 'roles.html', {'rol' : rol})

@login_required
def create_rol(request):
    if request.method == 'GET':
        activate(request.LANGUAGE_CODE)
        print (request.LANGUAGE_CODE)
        messages.get_messages(request)
        return render(request, 'new_rol.html',{
                                                'form': RolForm
                                             })
    else:
        form = RolForm(request.POST)
        
        del form.fields['rol_cod']
        if form.is_valid():
            new_rol = Rol(
                            rol_nombre = form.cleaned_data['rol_nombre'],
                            rol_descripcion = form.cleaned_data['rol_descripcion']
            )
            new_rol.save()
            msg =_('Rol creado con éxito.')
            messages.success(request, msg)
            return redirect('roles')
        else:
            print(form.errors)
            return render(request, 'new_rol.html',{
                                                'form': RolForm
                                             })

@login_required
def edit_rol(request):
    if request.method == 'GET':
        rol = Rol.objects.get( rol_cod = request.GET['rol_editID'])
        
        valores_por_defecto = {
            'rol_cod': rol.rol_cod,
            'rol_nombre': rol.rol_nombre,
            'rol_descripcion': rol.rol_descripcion,
        }

        editform = RolForm(initial=valores_por_defecto)

        return render(request, 'edit_rol.html',{
                                                'form': editform
                                             })
    else:

        rol = Rol.objects.get( rol_cod = request.POST['rol_cod'])
        form = RolForm(request.POST, instance=rol)
        if form.is_valid():
            # Guarda los cambios en el usuario
            form.save()
            msg = _('Rol actualizado.')
            messages.success(request, msg)
            return redirect('roles')

        return render(request, 'edit_rol.html', {'form': form, 'rol': rol}) 

@login_required
def delete_rol(request):
    if request.method == 'GET':
        roles(request)
    else:
        rol = Rol.objects.get( rol_cod = request.POST['rolID'])
        msg = _('Rol eliminado con éxito.')
        messages.success(request, msg)
        rol.delete()

    return redirect('/roles/') #añadr la ruta donde se vaya a redirigir

@login_required
def users(request):
    if request.user.is_authenticated:
        print('autenticado')
        usuario_actual = request.user
        # Acceder a la información del usuario

    user = Usuario.objects.all()
    messages.get_messages(request)
    return render(request, 'users.html', {'user' : user,
                                          'usuario_actual': usuario_actual})

@login_required
def delete_Usuario(request):
    if request.method == 'GET':
        users(request)
    else:
        usuario = Usuario.objects.get( id = request.POST['userID'])
        msg = _('Usuario eliminado con éxito.')
        messages.success(request, msg)
        usuario.delete()

    return redirect('/users/') #añadr la ruta donde se vaya a redirigir

#Funcion encargada de la edicion de la informacion del usuario
@login_required
def edit_usuario(request):
    if request.method == 'GET':
        usuario = Usuario.objects.get( id = request.GET['editID'])
        

        valores_por_defecto = {
            'username': usuario.username,
            'email': usuario.email,
            'first_name': usuario.first_name,
            'last_name': usuario.last_name,
            'user_per_tipo_doc': usuario.user_per_tipo_doc,
            'user_numero_doc': usuario.user_numero_doc,
            'user_telefono': usuario.user_telefono,
        }

        editform = CustomUserEditForm(initial=valores_por_defecto)

        return render(request, 'signupEdit.html',{
                                                'form': editform
                                             })
    else:

        usuario = Usuario.objects.get( username = request.POST['username'])
        form = CustomUserEditForm(request.POST, instance=usuario)
        if form.is_valid():
            # Guarda los cambios en el usuario
            form.save()
            msg = _('La información del usuario ha sido actualizada.')
            messages.success(request, msg)
            return redirect('users')

        return render(request, 'signupEdit.html', {'form': form, 'usuario': usuario})


#funcion para la creacion del usuario por medio de la interfaz inicial
# @login_required
def signup(request):
    #El GET se invoca al ingresar por primera vez a la pagina y envia el formulario
    if request.method == 'GET':
        messages.get_messages(request)
        return render(request, 'signup.html',{
                                                'form': CustomUserCreationForm
                                             })
    else:
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['password1'] == form.cleaned_data['password2']:
                try:
                    new_user = Usuario.objects.create_user(
                        username=form.cleaned_data['username'],
                        password=form.cleaned_data['password1'],
                        first_name=form.cleaned_data['first_name'],
                        last_name=form.cleaned_data['last_name'],
                        email=form.cleaned_data['email'],
                        user_per_tipo_doc=form.cleaned_data['tipo_doc'],
                        user_numero_doc=form.cleaned_data['num_doc'],
                        user_telefono=form.cleaned_data['num_tel'],
                        cod_rol=Rol.objects.get(rol_cod=form.cleaned_data['rol'])
                    )
                    new_user.save()
                    msg =_('Usuario creado con éxito.')
                    messages.success(request, msg)
                    return redirect('users')
                except IntegrityError:
                    messages.warning(request, 'Nombre de usuario ya existe.')
                    return render(request, 'signup.html',{
                                                'form': CustomUserCreationForm
                                             })
            else:
                msg = _('La contraseña no coincide.')
                messages.warning(request, msg)
                return render(request, 'signup.html',{
                                                'form': CustomUserCreationForm
                                             })
        else:
            # Captura los errores del formulario y procesa según tus necesidades
            errors = form.errors
            for field, error_list in errors.items():
                for error in error_list:
                    messages.warning(request, f'{field}: {error}')
            return render(request, 'signup.html',{
                                                'form': CustomUserCreationForm
                                             })
        
def inventory(request):
    return render(request, 'inventory.html')

def orders(request):
    return render(request, 'orders.html')

def cotizaciones(request):
    return render(request, 'cotizaciones.html')

def sales(request):
    return render(request, 'sales.html')

def reports(request):
    return render(request, 'reports.html')

def sucursales(request):
    return render(request, 'sucursales.html')


def create_Cargo(request):
    new_cargo = Cargo(
                        cargo_nombre = request.POST['cargo_nombre'],
                        cargo_descripcion = request.POST['cargo_descripcion'],
                        cargo_vigente = True
                    )
    new_cargo.save()

    return redirect('/rutapordefinir/') #añadr la ruta donde se vaya a redirigir


def create_Sucursal(request):
    new_sucursal = Sucursal(
                        sucursal_nombre = request.POST['surcursal_nombre'],
                        sucursal_ubicacion = request.POST['surcursal_ubicacion'],
                        sucursal_cod_gerente = request.POST['surcursal_gerente'],
                        sucursal_vigente = True
                        )
    new_sucursal.save()

    return redirect('/rutapordefinir/') #añadr la ruta donde se vaya a redirigir

def create_PersonaxCargo(request):
    new_personaxcargo = PersonaXCargo(
                                        perxcargo_persona_cod = request.POST['perxcargo_persona'],
                                        perxcargo_cargo_cod =  request.POST['perxcargo_cargo'],
                                        perxcargo_sucursal_cod = request.POST['perxcargo_sucursal'],
                                        perxcargo_vigente = True
                                    )
    new_personaxcargo.save()

    return redirect('/rutapordefinir/') #añadr la ruta donde se vaya a redirigir

def create_Menu(request):
    new_menu = Menu(
                    menu_nombre = request.POST['menu_nombre'],
                    menu_descripcion = request.POST['menu_descripcion'],
                    menu_estado = request.POST['menu_estado'],
                    menu_vigente = True
                    )
    new_menu.save()

    return redirect('/rutapordefinir/') #añadr la ruta donde se vaya a redirigir

def create_Permiso(request):
    new_permiso = Permiso(
                        permiso_cod_menu = request.POST['permiso_menu'],
                        permiso_cod_rol = request.POST['permiso_rol'],
                        permiso_read = request.POST['permiso_read'],
                        permiso_write = request.POST['permiso_write'],
                        permiso_update = request.POST['permiso_update'],
                        permiso_delete = request.POST['permiso_delete'],
                        permiso_vigente = True 
                        )
    new_permiso.save()

    return redirect('/rutapordefinir/') #añadr la ruta donde se vaya a redirigir

def create_VehiculoVenta(request):
    new_vehiculoventa = VehiculoVenta(
                                        vehvnt_placa = request.POST['vehvnt_placa'],
                                        vehvnt_marca = request.POST['vehvnt_marca'],
                                        vehvnt_color = request.POST['vehvnt_color'],
                                        vehvnt_anio = request.POST['vehvnt_anio'],
                                        vehvnt_cod_sucursal = request.POST['vehvnt_sucursal'],
                                        vehvnt_precioneto = request.POST['vehvnt_precioneto'],
                                        vehvnt_disponible = request.POST['vehvnt_disponible'],
                                        vehvnt_vigente = True
                                    )
    new_vehiculoventa.save()

    return redirect('/rutapordefinir/') #añadr la ruta donde se vaya a redirigir

def create_VehiculoReparacion(request):
    new_vehiculoreparacion = VehiculoReparacion(
                                                    vehrep_placa = request.POST['vehrep_placa'],
                                                    vehrep_marca = request.POST['vehrep_marca'],
                                                    vehrep_color = request.POST['vehrep_color'],
                                                    vehrep_enReparacion = request.POST['vehrep_reparado'],
                                                    vehrep_dueño = request.POST['vehrep_dueño'],
                                                    vehrep_vigente = True
                                                )
    new_vehiculoreparacion.save()

    return redirect('/rutapordefinir/') #añadr la ruta donde se vaya a redirigir

def create_OrdenTrabajo(request):
    new_ordentrabajo = OrdenTrabajo(
                                        orden_vehiculoreparacion = request.POST['orden_vehiculoreparacion'],
                                        orden_encargado = request.POST['orden_encargado'],
                                        orden_observacion = request.POST['orden_observacion'],
                                        orden_estado = request.POST['orden_estado'],
                                        orden_vigente = True
                                    )
    new_ordentrabajo.save()

    return redirect('/rutapordefinir/') #añadr la ruta donde se vaya a redirigir

def create_Inventario(request):
    new_inventario = Inventario(
                                    inv_nombre = request.POST['inv_nombre'],
                                    inv_categoria = request.POST['inv_categoria'],
                                    inv_descripcion = request.POST['inv_descripcion'],
                                    inv_precioneto = request.POST['inv_precioneto'],
                                    inv_vigente = True
                                )
    new_inventario.save()

    return redirect('/rutapordefinir/') #añadr la ruta donde se vaya a redirigir

def create_InventarioPorSucursal(request):
    new_inventarioporsucursal = InventarioPorSucursal(
                                                        invssus_codigo_inventario = request.POST['invssus_inventario'],
                                                        invsus_sucursal = request.POST['invsus_sucursal'],
                                                        invss_existencias = request.POST['invss_existencias'],
                                                        inv_vigente = True
                                                    )
    new_inventarioporsucursal.save()

    return redirect('/rutapordefinir/') #añadr la ruta donde se vaya a redirigir

def create_CotizacionReparacion(request):
    new_cotizacionreparacion = CotizacionReparacion(
                                                        cotrep_orden_trabajo = request.POST['cotrep_ordentrabajo'],
                                                        cotrep_precioreparacion = request.POST['precioreparacion'],
                                                        cotrep_observaciones = request.POST['observaciones'],
                                                        cotrep_fecharealizada = request.POST['cotrep_fecharealizada'],
                                                        cotrep_estado = request.POST['cotrep_estado'],
                                                        cotrep_vigente = True
                                                    )
    new_cotizacionreparacion.save()

    return redirect('/rutapordefinir/') #añadr la ruta donde se vaya a redirigir

def create_RepuestoVenta(request):
    new_repuestoventa = RepuestoVenta(
                                        cotrepues_repuestocod = request.POST['cotrepues_repuesto'],
                                        cotrepues_preciotemporal = request.POST['preciotemporal'],
                                        cotrepues_fecharealizada = request.POST['cotrepues_fecharealizada'],
                                        cotrepues_estado = request.POST['cotrepues_estado'],
                                        cotrepues_vigente = True
                                    )
    new_repuestoventa.save()

    return redirect('/rutapordefinir/') #añadr la ruta donde se vaya a redirigir

def create_CotizacionVehiculo(request):
    new_cotizacionvehiculo = CotizacionVehiculo(
                                                    cotven_cod_vehiculo_nuevo = request.POST['cotven_vehiculonuevo'],
                                                    cotven_fecharealizada = request.POST['cotven_fecharealizada'],
                                                    cotven_estado = request.POST['cotven_estado'],
                                                    cotven_vigente = True
                                                )
    new_cotizacionvehiculo.save()

    return redirect('/rutapordefinir/') #añadr la ruta donde se vaya a redirigir

def create_Factura(request):
    new_factura = Factura(
                            codfac_cliente = request.POST['cliente'],
                            codfac_vendedor = request.POST['vendedor'],
                            codfac_cotizacion_vehiculonuevo = request.POST['cod_cotizacion_vehiculonuevo'],
                            codfac_reparacion = request.POST['cod_reparacion'],
                            codfac_repuestos = request.POST['cod_repuestos'],
                            codfac_subtotal = request.POST['subtotal'],
                            codfac_iva = request.POST['iva'],
                            codfac_descuento = request.POST['descuento'],
                            codfac_precioTotal = request.POST['precioTotal'],
                            codfac_fecharealizada = request.POST['codfac_fecharealizada'],
                            codfac_vigente = True
                        )
    new_factura.save()

    return redirect('/rutapordefinir/') #añadr la ruta donde se vaya a redirigir

#FIN SECCION DE INSERCIONES

#SECCION DE BORRADOS EN LAS TABLAS DE LA BD
    return redirect('/rutapordefinir/') #añadr la ruta donde se vaya a redirigir

def delete_Cargo(request, cargo_id):
    cargo = Cargo.objects.get( cargo_cod = cargo_id)
    cargo.delete()

    return redirect('/rutapordefinir/') #añadr la ruta donde se vaya a redirigir

def delete_Sucursal(request, sucursal_id):
    sucursal = Sucursal.objects.get( sucursal_cod = sucursal_id)
    sucursal.delete()

    return redirect('/rutapordefinir/') #añadr la ruta donde se vaya a redirigir

def delete_PersonaxCargo(request, personaxcarg_id):
    personaxcargo = PersonaXCargo.objects.get( perxcargo_cod = personaxcarg_id)
    personaxcargo.delete()

    return redirect('/rutapordefinir/') #añadr la ruta donde se vaya a redirigir

def delete_Menu(request, menuid):
    menu = Menu.objects.get( menu_id = menuid)
    menu.delete()

    return redirect('/rutapordefinir/') #añadr la ruta donde se vaya a redirigir

def delete_Permiso(request, permisoid):
    permiso = Permiso.objects.get( permiso_id = permisoid)
    permiso.delete()

    return redirect('/rutapordefinir/') #añadr la ruta donde se vaya a redirigir

def delete_VehiculoVenta(request, vehiculoventa_id):
    vehiculoventa = VehiculoVenta.objects.get( vehvnt_cod = vehiculoventa_id)
    vehiculoventa.delete()

    return redirect('/rutapordefinir/') #añadr la ruta donde se vaya a redirigir

def delete_VehiculoReparacion(request, vehiculoreparacion_id):
    vehiculoreparacion = VehiculoReparacion.objects.get( vehrep_cod = vehiculoreparacion_id)
    vehiculoreparacion.delete()

    return redirect('/rutapordefinir/') #añadr la ruta donde se vaya a redirigir

def delete_OrdenTrabajo(request, orden_id):
    ordentrabajo = OrdenTrabajo.objects.get( orden_cod = orden_id)
    ordentrabajo.delete()

    return redirect('/rutapordefinir/') #añadr la ruta donde se vaya a redirigir

def delete_Inventario(request, inventario_id):
    inventario = Inventario.objects.get( inv_cod = inventario_id)
    inventario.delete()

    return redirect('/rutapordefinir/') #añadr la ruta donde se vaya a redirigir

def delete_InventarioPorSucursal(request, inventarioSurcursal_id):
    inventarioporsucursal = InventarioPorSucursal.objects.get( invsus_cod = inventarioSurcursal_id)
    inventarioporsucursal.delete()

    return redirect('/rutapordefinir/') #añadr la ruta donde se vaya a redirigir

def delete_CotizacionReparacion(request, cotizacionRep_id):
    cotizacionreparacion = CotizacionReparacion.objects.get( cotrep_cod = cotizacionRep_id)
    cotizacionreparacion.delete()

    return redirect('/rutapordefinir/') #añadr la ruta donde se vaya a redirigir

def delete_RepuestoVenta(request, repuestoventa_id):
    repuestoventa = RepuestoVenta.objects.get( repvnt_cod = repuestoventa_id)
    repuestoventa.delete()

    return redirect('/rutapordefinir/') #añadr la ruta donde se vaya a redirigir

def delete_CotizacionVehiculo(request, cotizacionvehiculo_id):
    cotizacionvehiculo = CotizacionVehiculo.objects.get( cotven_cod = cotizacionvehiculo_id)
    cotizacionvehiculo.delete()

    return redirect('/rutapordefinir/') #añadr la ruta donde se vaya a redirigir

def delete_Factura(request, fac_id):
    factura = Factura.objects.get( codfac = fac_id)
    factura.delete()

    return redirect('/rutapordefinir/') #añadr la ruta donde se vaya a redirigir

#FIN SECCION BORRADOS

def cambiar_idioma(request, idioma):
    if idioma in dict(settings.LANGUAGES):
        activate(idioma)
        response = HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        response.set_cookie('django_language', idioma)
        return response
    else:
        return HttpResponseRedirect('/')
