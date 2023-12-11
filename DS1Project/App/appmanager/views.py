from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.db import IntegrityError
from django.utils.translation import gettext as _, activate
from django.conf import settings
from .models import *
from .forms import *


def home(request):
    print (request.LANGUAGE_CODE)
    return render(request, "home.html")


@login_required
def adminpage(request):
    actual_user = request.user
    users_count = Usuario.objects.count()
    products_count = Inventario.objects.count()
    branches_count = Sucursal.objects.count()

    return render(request, 'adminpage.html', {
        'actual_user': actual_user, 
        'users_count': users_count, 
        'products_count': products_count, 
        'branches_count': branches_count
        }
    )


def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('adminpage')
            else:
                messages.error(request, _('Username o contraseña incorrecta.'))
                return redirect('login')
            
        else:
            # Verifica los errores específicos del formulario
            if 'captcha' in form.errors:
                captcha_error = _("Debe superar la prueba reCAPTCHA")
                messages.error(request, captcha_error)
            else:
                for error in form.errors.values():
                    messages.error(request, _(error))
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})


def exit(request):
    logout(request)
    return redirect('home')


def roles(request):
    rol = Rol.objects.all()
    messages.get_messages(request)
    return render(request, 'roles.html', {'rol' : rol})


@login_required
def create_rol(request):
    if request.method == 'GET':
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

    return redirect('/roles/')


@login_required
def users(request):
    if request.user.is_authenticated:
        usuario_actual = request.user

        if usuario_actual.cod_rol.rol_cod == 3:
            listado_usuarios = Usuario.objects.filter(cod_rol_id = 5)

            for usuario in listado_usuarios:
            # Obtén el objeto PersonaXCargo relacionado con el usuario actual
                persona_cargo = PersonaXCargo.objects.filter(perxcargo_persona_cod=usuario).first()

                # Verifica si se encontró un objeto PersonaXCargo
                if persona_cargo:
                    # Accede a los campos que necesitas (rol_cod y cargo_cod)
                    sucursal_cod = persona_cargo.perxcargo_sucursal_cod.sucursal_nombre
                    cargo_cod = persona_cargo.perxcargo_cargo_cod.cargo_nombre

                    # Agrega estos valores al contexto del usuario
                    usuario.sucursal_cod = sucursal_cod
                    usuario.cargo_cod = cargo_cod
                else:
                    # Si no se encuentra una entrada en PersonaXCargo, establece valores predeterminados o maneja la situación según sea necesario
                    usuario.sucursal_cod = None
                    usuario.cargo_cod = None

        else:
            listado_usuarios = Usuario.objects.all()

            for usuario in listado_usuarios:
        # Obtén el objeto PersonaXCargo relacionado con el usuario actual
                persona_cargo = PersonaXCargo.objects.filter(perxcargo_persona_cod=usuario).first()

                # Verifica si se encontró un objeto PersonaXCargo
                if persona_cargo:
                    # Accede a los campos que necesitas (rol_cod y cargo_cod)
                    sucursal_cod = persona_cargo.perxcargo_sucursal_cod.sucursal_nombre
                    cargo_cod = persona_cargo.perxcargo_cargo_cod.cargo_nombre

                    # Agrega estos valores al contexto del usuario
                    usuario.sucursal_cod = sucursal_cod
                    usuario.cargo_cod = cargo_cod
                else:
                    # Si no se encuentra una entrada en PersonaXCargo, establece valores predeterminados o maneja la situación según sea necesario
                    usuario.sucursal_cod = None
                    usuario.cargo_cod = None

    messages.get_messages(request)
    return render(request, 'users.html', {'listado_usuarios' : listado_usuarios,
                                          'usuario_actual': request.user})


@login_required
def delete_Usuario(request):
    if request.method == 'GET':
        users(request)
    else:
        usuario = Usuario.objects.get( id = request.POST['userID'])
        msg = _('Usuario eliminado con éxito.')
        messages.success(request, msg)
        usuario.delete()

    return redirect('/users/')


#Funcion encargada de la edicion de la informacion del usuario
@login_required
def edit_usuario(request):
    if request.method == 'GET':
        usuario = Usuario.objects.get( id = request.GET['editID'])

        if request.user and (request.user.cod_rol.rol_cod == 2 or request.user.cod_rol.rol_cod == 1):
            CustomUserEditForm.base_fields['cod_rol'].queryset = Rol.objects.all()
            #CustomUserEditForm.base_fields['cod_cargo'].queryset = Cargo.objects.all()
        elif request.user and request.user.cod_rol.rol_cod == 3:
            CustomUserEditForm.base_fields['cod_rol'].queryset = Rol.objects.filter(rol_cod = 5)
            #CustomUserEditForm.base_fields['cod_cargo'].queryset = Cargo.objects.filter( cargo_cod = 4)
        else:
            CustomUserEditForm.base_fields['cod_rol'].queryset = Rol.objects.none()
            #CustomUserEditForm.base_fields['cod_cargo'].queryset = Cargo.objects.none()

        editform = CustomUserEditForm(instance=usuario)

        editform.fields.pop('password') #elimina el campos de password porque no se utiliza

        return render(request, 'signupEdit.html',{
                                                'form': editform
                                             })
    else:

        usuario = Usuario.objects.get( username = request.POST['username'])

        if request.user and (request.user.cod_rol.rol_cod == 2 or request.user.cod_rol.rol_cod == 1):
            CustomUserEditForm.base_fields['cod_rol'].queryset = Rol.objects.all()
            
        elif request.user and request.user.cod_rol.rol_cod == 3:
            CustomUserEditForm.base_fields['cod_rol'].queryset = Rol.objects.filter(rol_cod = 5)
            
        else:
            CustomUserEditForm.base_fields['cod_rol'].queryset = Rol.objects.none()
            #CustomUserEditForm.base_fields['cod_cargo'].queryset = Cargo.objects.none()

        CustomUserEditForm.base_fields['cod_sucursal'].initial = request.POST.get('cod_sucursal', None)

        form = CustomUserEditForm(request.POST, instance=usuario)
        if form.is_valid():
            # Guarda los cambios en el usuario
            form.save()
            msg = _('La información del usuario ha sido actualizada.')
            messages.success(request, msg)
            return redirect('users')

        return render(request, 'signupEdit.html', {'form': form, 'usuario': usuario})


#funcion para la creacion del usuario por medio de la interfaz inicial
@login_required
def signup(request):
    #El GET se invoca al ingresar por primera vez a la pagina y envia el formulario
    if request.method == 'GET':
        form = CustomUserCreationForm(request.POST or None, user = request.user)
        messages.get_messages(request)
        return render(request, 'signup.html',{
                                                'form': form
                                             })
    else:
        form = CustomUserCreationForm(request.POST or None, user = request.user)
        if form.is_valid():

            def create_PersonaXCargo(user, selected_branch):
                role_to_position = {
                    'Superadministrador': 'Gerente',  # Asignando el cargo de Gerente a los Superadministradores
                    'Gerente': 'Gerente',
                    'Vendedor': 'Vendedor',
                    'Jefe de taller': 'Jefe de taller',
                    'Cliente': 'Cliente'
                }
                name_position = role_to_position.get(user.cod_rol.rol_nombre, None)

                if name_position is not None:
                    position_found = Cargo.objects.filter(cargo_nombre=name_position).first()

                    if position_found:
                        persona_por_cargo = PersonaXCargo(
                            perxcargo_persona_cod_id=user.id,
                            perxcargo_cargo_cod_id=position_found.cargo_cod,
                            perxcargo_sucursal_cod=selected_branch,  # Asigna la sucursal correspondiente
                            perxcargo_vigente=True,
                        )
                        persona_por_cargo.save()

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
                    selected_branch = form.cleaned_data['cod_sucursal']
                    create_PersonaXCargo(new_user, selected_branch)
                    msg =_('Usuario creado con éxito.')
                    messages.success(request, msg)
                    return redirect('users')
                except IntegrityError:
                    form = CustomUserCreationForm(request.POST or None, user=request.user)
                    messages.warning(request, 'Nombre de usuario ya existe.')
                    return render(request, 'signup.html',{
                                                'form': form
                                             })
            else:
                form = CustomUserCreationForm(request.POST or None, user=request.user)
                msg = _('La contraseña no coincide.')
                messages.warning(request, msg)
                return render(request, 'signup.html',{
                                                'form': form
                                             })
        else:
            form = CustomUserCreationForm(request.POST or None, user=request.user)
            # Captura los errores del formulario y procesa según tus necesidades
            errors = form.errors
            for field, error_list in errors.items():
                for error in error_list:
                    messages.warning(request, f'{field}: {error}')
            return render(request, 'signup.html',{
                                                'form': form
                                             })


def inventory(request):
    sucursal_usuario = PersonaXCargo.objects.get(perxcargo_persona_cod=request.user)

    if request.user.cod_rol.rol_cod == 1:
        inventario = InventarioPorSucursal.objects.all()
    else:
        inventario = InventarioPorSucursal.objects.filter(invsus_sucursal = sucursal_usuario.perxcargo_sucursal_cod)

    messages.get_messages(request)
    return render(request, 'inventory.html', {'inventario': inventario})


def orders(request):
    orders = OrdenTrabajo.objects.all()

    vehicle_repair = VehiculoReparacion.objects.all()
    
    # Crear un diccionario para mapear los dueños por orden de trabajo
    owners = {vehicle.vehrep_cod: vehicle.vehrep_dueño.username for vehicle in vehicle_repair}
    
    # Asociar los dueños de los vehículos a cada orden de trabajo
    for order in orders:
        order.orden_dueño = owners.get(order.orden_vehiculoreparacion_id)
    
    messages.get_messages(request)
    return render(request, 'orders.html', {'orders': orders})


def cerrar_orden_trabajo(request):

    orden = OrdenTrabajo.objects.get(orden_cod = request.POST['orden_closeID'])

    # Cambiar el estado de orden_estado
    orden.orden_estado = not orden.orden_estado  # Cambia el estado a su opuesto
    orden.save()

    # Cambiar el estado de vehrep_enReparacion
    vehiculo = orden.orden_vehiculoreparacion
    vehiculo.vehrep_enReparacion = not vehiculo.vehrep_enReparacion  # Cambia el estado a su opuesto
    vehiculo.save()

    msg = _('Orden de trabajo finalizada.')
    messages.success(request, msg)

    return redirect('orders') 


def cotizaciones(request):
    if request.user.cod_rol.rol_cod == 5:
        cotizaciones = CotizacionReparacion.objects.filter(cotrep_orden_trabajo__orden_vehiculoreparacion__vehrep_dueño=request.user)
    else:
        cotizaciones = CotizacionReparacion.objects.all()

    return render(request, 'cotizaciones.html', {'cotizaciones': cotizaciones})


@login_required
def cambiar_estado_cotizacion(request):

    cotizacion = CotizacionReparacion.objects.get(cotrep_cod = request.POST['acept_ID'])

    if request.user == cotizacion.cotrep_orden_trabajo.orden_vehiculoreparacion.vehrep_dueño:
        # Cambia el estado de la cotización
        cotizacion.cotrep_estado = not cotizacion.cotrep_estado  # Cambia el estado al contrario del actual
        cotizacion.save()

        # Mensaje de éxito
        msg = _('La cotización ha sido aprobada.')
        messages.success(request, msg)
        return redirect('cotizaciones')  

    else:
        msg = _('Algo falló al aprobar la cotización')
        messages.error(request, msg)
        return redirect('cotizaciones')


def sales(request):
    return render(request, 'sales.html')


def reports(request):
    return render(request, 'reports.html')


def sucursales(request):
    sucursales = Sucursal.objects.all()
    messages.get_messages(request)
    return render(request, 'sucursales.html', {'sucursales' : sucursales})


def create_sucursal(request):
    if request.method == 'GET':
        form = SucursalForm()
        return render(request, 'new_sucursal.html', {'form': form})
    
    else:
        form = SucursalForm(request.POST)

        form.fields.pop('sucursal_cod', None)

        if form.is_valid():
            form = form.save()
            msg =_('Sucursal creada con éxito.')
            messages.success(request, msg)
            return redirect('sucursales')
            
        else:
            # Captura los errores del formulario
            errors = form.errors
            for field, error_list in errors.items():
                for error in error_list:
                    messages.warning(request, f'{field}: {error}')
                    
            return render(request, 'sucursales.html',{
                                                'form': form
                                             })


def edit_sucursal(request):
    if request.method == 'GET':
        sucursal = Sucursal.objects.get( sucursal_cod = request.GET['sucursal_editID'])
        
        valores_por_defecto = {
            'sucursal_cod': sucursal.sucursal_cod,
            'sucursal_nombre': sucursal.sucursal_nombre,
            'sucursal_ubicacion': sucursal.sucursal_ubicacion,
            'sucursal_cod_gerente': sucursal.sucursal_cod_gerente,
        }

        editform = SucursalForm(initial=valores_por_defecto)

        return render(request, 'edit_sucursal.html',{
                                                'form': editform
                                             })
    else:
        sucursal = Sucursal.objects.get( sucursal_cod = request.POST['sucursal_cod'])
        form = SucursalForm(request.POST, instance=sucursal)
        if form.is_valid():
            # Guarda los cambios en el usuario
            form.save()
            msg = _('Sucursal actualizada.')
            messages.success(request, msg)
            return redirect( 'sucursales' )
        else:
            errors = form.errors
            for field, error_list in errors.items():
                for error in error_list:
                    messages.warning(request, f'{field}: {error}')
                
            return render(request, 'edit_sucursal.html', {'form': form, 'sucursal': sucursal}) 


def edit_product(request):
    if request.method == 'GET':
        product = Inventario.objects.get( inv_cod = request.GET['product_editID'])
        
        valores_por_defecto = {
            'inv_cod': product.inv_cod,
            'inv_nombre': product.inv_nombre,
            'inv_categoria': product.inv_categoria,
            'inv_precioneto': product.inv_precioneto,
            'inv_vigente': product.inv_vigente,
            'inv_categoria': product.inv_categoria,
        }

        editform = EditarProductoForm(initial=valores_por_defecto)

        return render(request, 'edit_product.html',{
                                                'form': editform
                                             })
    else:

        product = Inventario.objects.get( inv_cod = request.POST['inv_cod'])
        form = EditarProductoForm(request.POST, instance=product)
        if form.is_valid():
            # Guarda los cambios en el usuario
            form.save()
            msg = _('Producto actualizado.')
            messages.success(request, msg)
            return redirect('inventory')

        return render(request, 'edit_product.html', {'form': form, 'product': product}) 


def delete_Sucursal(request):
    if request.method == 'GET':
        sucursales(request)
    else:
        sucursal = Sucursal.objects.get( sucursal_cod = request.POST['delete_sucursalID'])
        msg = _('Sucursal eliminada con éxito.')
        messages.success(request, msg)
        sucursal.delete()

    return redirect( 'sucursales' ) 


def create_Cargo(request):
    new_cargo = Cargo(
                        cargo_nombre = request.POST['cargo_nombre'],
                        cargo_descripcion = request.POST['cargo_descripcion'],
                        cargo_vigente = True
                    )
    new_cargo.save()

    return redirect('/rutapordefinir/') #añadr la ruta donde se vaya a redirigir


def create_vehiculoVenta(request):
    if request.method == 'POST':
        form = VehiculoVentaForm(request.POST)
        if form.is_valid():
            # Realizar acciones cuando el formulario es válido
            # Guardar el formulario, enviar notificaciones, etc.
            form.save()
            # Redirigir a la página de inventario u otra página deseada
            return HttpResponseRedirect('/inventory/')  # Cambia '/inventario/' por la URL a la que quieres redirigir
    else:
        form = VehiculoVentaForm()
        
    return render(request, 'new_vehicle.html', {'form': form})


def create_order(request):
    if request.method == 'POST':
        form = OrdenTrabajoVehiculoForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirigir a alguna página de éxito o a donde desees
            return redirect('orders')
    else:
        form = OrdenTrabajoVehiculoForm()

    return render(request, 'new_order.html', {'form': form})


def create_product(request):
    if request.method == 'POST':
        form = CrearProductoForm(request.POST)
        if form.is_valid():
            nuevo_producto = form.save(commit=False)
            categoria_seleccionada = form.cleaned_data['categoria']

            # Asignar la categoría seleccionada al nuevo producto
            nuevo_producto.inv_categoria = categoria_seleccionada
            nuevo_producto.save()

            # Obtener la sucursal seleccionada del formulario
            sucursal_seleccionada = form.cleaned_data['sucursal']

            # Crear o actualizar la entrada en InventarioPorSucursal
            InventarioPorSucursal.objects.update_or_create(
                invsus_codigo_inventario=nuevo_producto,
                invsus_sucursal=sucursal_seleccionada,
                defaults={'invsus_existencias': form.cleaned_data['existencias']}
            )

            # Redirigir a alguna página de éxito
            return redirect('inventory')

    else:
        form = CrearProductoForm()
    
    return render(request, 'new_product.html', {'form': form})


def create_CotizacionReparacion(request):
    #AÑADIR EL RESTO DE LOGICO DEL PROCESAMIENTO DEL FORMULARIO
    if request.method == 'GET':
        messages.get_messages(request)
        return render(request, 'cotizar_reparacion.html',{
                                                'form': CotizacionReparacionForm
                                             })
    else:
        form = CotizacionReparacionForm(request.POST)
        form.fields.pop('cotrep_cod', None)

        if form.is_valid():
            form.save()
            msg =_('Cotización creada con éxito.')
            messages.success(request, msg)
            return redirect('cotizaciones')
        else:
            print(form.errors)
            return render(request, 'cotizar_reparacion.html',{
                                                'form': CotizacionReparacionForm
                                             })
        

def edit_order(request):
    if request.method == 'GET':
        order = OrdenTrabajo.objects.get(orden_cod=request.GET['order_editID'])
        
        valores_por_defecto = {
            'orden_cod': order.orden_cod,
            'orden_vehiculoreparacion': order.orden_vehiculoreparacion,
            'orden_encargado': order.orden_encargado,
            'orden_observacion': order.orden_observacion,
            'orden_estado': order.orden_estado,
            'orden_vigente': order.orden_vigente,
        }

        edit_form = EditarOrdenTrabajoForm(initial=valores_por_defecto)

        return render(request, 'edit_order.html', {'form': edit_form})
    
    else:
        order = OrdenTrabajo.objects.get(orden_cod=request.POST['orden_cod'])
        form = EditarOrdenTrabajoForm(request.POST, instance=order)
        
        if form.is_valid():
            form.save()
            msg = _('Orden actualizada.')
            messages.success(request, msg)
            return redirect('orders')  # Cambia esto a la URL correcta

        return render(request, 'edit_order.html', {'form': form, 'order': order})


def edit_cotizacion_reparacion(request):
    if request.method == 'GET':
        cotrep = CotizacionReparacion.objects.get( cotrep_cod = request.GET['edit_cotID'])

        valores_por_defecto = {
            'cotrep_cod': cotrep.cotrep_cod,
            'cotrep_orden_trabajo': cotrep.cotrep_orden_trabajo,
            'cotrep_precioreparacion': cotrep.cotrep_precioreparacion,
            'cotrep_observaciones': cotrep.cotrep_observaciones,
        }

        editform = CotizacionReparacionForm(initial=valores_por_defecto)

        return render(request, 'edit_cotizacion_reparacion.html',{
                                                'form': editform
                                             })
    else:
        print (request.POST)
        cotrep = CotizacionReparacion.objects.get( cotrep_cod = request.POST['cotrep_cod'])
        form = CotizacionReparacionForm(request.POST, instance=cotrep)
        if form.is_valid():
            # Guarda los cambios en el usuario
            form.save()
            msg = _('Cotización de reparación actualizada.')
            messages.success(request, msg)
            return redirect( 'cotizaciones' )
        else:
            errors = form.errors
            for field, error_list in errors.items():
                for error in error_list:
                    messages.warning(request, f'{field}: {error}')
                
            return render(request, 'edit_cotizacion_reparacion.html', {'form': form, 'cotizacion': cotrep})


def delete_CotizacionReparacion(request):
    if request.method == 'GET':
        cotizaciones(request)
    else:
        cotrep = CotizacionReparacion.objects.get( cotrep_cod = request.POST['delete_cotID'])
        cotrep.delete()
        msg = _('La cotización de reparación fue eliminada con éxito.')
        messages.success(request, msg)

    return redirect( 'cotizaciones' ) 


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
def delete_Cargo(request, cargo_id):
    cargo = Cargo.objects.get( cargo_cod = cargo_id)
    cargo.delete()

    return redirect('/rutapordefinir/') #añadr la ruta donde se vaya a redirigir


def delete_PersonaxCargo(request, personaxcarg_id):
    personaxcargo = PersonaXCargo.objects.get( perxcargo_cod = personaxcarg_id)
    personaxcargo.delete()

    return redirect('/rutapordefinir/') #añadr la ruta donde se vaya a redirigir


def delete_vehiculoventa(request):
    if request.method == 'GET':
        view_vehicle(request)
    else:
        vehicle = VehiculoVenta.objects.get(vehvnt_cod = request.POST['delete_vehicleID'])
        msg = _('Vehiculo eliminado con éxito.')
        messages.success(request, msg)
        vehicle.delete()

    return redirect( 'vehicle_inventory' )


def delete_VehiculoReparacion(request, vehiculoreparacion_id):
    vehiculoreparacion = VehiculoReparacion.objects.get( vehrep_cod = vehiculoreparacion_id)
    vehiculoreparacion.delete()

    return redirect('/rutapordefinir/') #añadr la ruta donde se vaya a redirigir


def delete_order(request):
    if request.method == 'GET':
        orders(request)
    else:
        ordentrabajo = OrdenTrabajo.objects.get( orden_cod = request.POST['delete_orderID'])
        msg = _('Orden eliminada con éxito.')
        messages.success(request, msg)
        ordentrabajo.delete()

    return redirect( 'orders' )


def delete_product(request):
    if request.method == 'GET':
        inventory(request)
    else:
        product = Inventario.objects.get(inv_cod = request.POST['delete_productID'])#
        msg = _('Producto eliminado con éxito.')
        messages.success(request, msg)
        product.delete()

    return redirect( 'inventory' )


def delete_InventarioPorSucursal(request, inventarioSurcursal_id):
    inventarioporsucursal = InventarioPorSucursal.objects.get( invsus_cod = inventarioSurcursal_id)
    inventarioporsucursal.delete()

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
    

def data_adminpage(request):
    users_count = Usuario.objects.count()
    products_count = Inventario.objects.count()

    return render(request, 'adminpage.html', {'users_count': users_count, 'products_count': products_count})


def consulta_reparacion_cliente(request):
    # Suponiendo que tienes un usuario autenticado
    usuario_actual = request.user

    # Obtener el vehículo más reciente asociado al usuario actual
    vehiculo_usuario = VehiculoReparacion.objects.filter(vehrep_dueño=usuario_actual).order_by('-create_at').first()

    # Obtener la orden de trabajo asociada al vehículo
    orden_trabajo = vehiculo_usuario.ordentrabajo_set.first()

    # Verificar si hay una cotización asociada a la orden de trabajo
    cotizacion = None
    if orden_trabajo:
        cotizacion = orden_trabajo.cotizacionreparacion_set.first()

    # Renderizar la plantilla con la información
    return render(request, 'consulta_reparacion.html', {'usuario': usuario_actual, 'vehiculo': vehiculo_usuario, 'orden_trabajo': orden_trabajo, 'cotizacion': cotizacion})


def view_vehicle(request):

    vehicles = VehiculoVenta.objects.all()

    messages.get_messages(request)
    return render(request, 'vehicle_inventory.html', {'vehicles': vehicles})

