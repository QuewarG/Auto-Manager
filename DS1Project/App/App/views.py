from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

# FUNCIONES DEL SISTEMA

def home(request):
    return render(request, 'home.html')

@login_required
def adminpage(request):
    return render(request, "adminpage.html")

def exit(request):
    logout(request)
    return redirect('home')

#Falta todo el direccionamiento de las rutas aqui y en el archivo de urls
#Lo que hay dentro de .POST['persona_apellido'] corresponde al name que le debes colocar a los campos del formulario

#CREACION DE LAS FUNCIONES PARA LA INSERCION DE LOS DATOS EN LAS TABLAS DE LA BD
def create_Persona(request):
    new_persona = Persona(
                        per_apellido = request.POST['persona_apellido'],
                        per_nombre = request.POST['persona_nombre'],
                        per_tipo_doc = request.POST['persona_tipo_doc'],
                        per_numero_doc = request.POST['persona_numeroDoc'],
                        per_correo = request.POST['persona_correo'],
                        per_telefono = request.POST['persona_telefono'],
                        per_vigente = True
                        )
    new_persona.save()

    return redirect('/rutapordefinir/') #añadr la ruta donde se vaya a redirigir

def create_Cargo(request):
    new_cargo = Cargo(
                        cargo_nombre = request.POST['cargo_nombre'],
                        cargo_descripcion = request.POST['cargo_descripcion'],
                        cargo_vigente = True
                    )
    new_cargo.save()

    return redirect('/rutapordefinir/') #añadr la ruta donde se vaya a redirigir

def create_Rol(request):
    new_rol = Rol(
                    rol_nombre = request.POST['rol_nombre'],
                    rol_descripcion = request.POST['rol_descripcion'],
                    rol_vigente = True
                )
    new_rol.save()

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

def create_Usuario(request):
    new_usuario = Usuario(
                            usuario_persona_cod = request.POST['usuario_persona'],
                            usuario_nickname = request.POST['usuario_nickname'],
                            usuario_correo = request.POST['usuario_correo'],
                            usuario_password = request.POST['usuario_password'],
                            usuario_cod_rol = request.POST['usuario_rol'],
                            usuario_cod_sucursal = request.POST['usuario_sucursal'],
                            usuario_ultima_conexion = request.POST['usuario_ultima_conexion'],
                            usuario_vigente = True
                        )
    new_usuario.save()

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

def delete_Persona(request, persona_id):
    persona = Persona.objects.get( per_cod = persona_id)
    persona.delete()

    return redirect('/rutapordefinir/') #añadr la ruta donde se vaya a redirigir

def delete_Cargo(request, cargo_id):
    cargo = Cargo.objects.get( cargo_cod = cargo_id)
    cargo.delete()

    return redirect('/rutapordefinir/') #añadr la ruta donde se vaya a redirigir

def delete_Rol(request, rol_id):
    rol = Rol.objects.get( rol_cod = rol_id)
    rol.delete()

    return redirect('/rutapordefinir/') #añadr la ruta donde se vaya a redirigir

def delete_Sucursal(request, sucursal_id):
    sucursal = Sucursal.objects.get( sucursal_cod = sucursal_id)
    sucursal.delete()

    return redirect('/rutapordefinir/') #añadr la ruta donde se vaya a redirigir

def delete_PersonaxCargo(request, personaxcarg_id):
    personaxcargo = PersonaXCargo.objects.get( perxcargo_cod = personaxcarg_id)
    personaxcargo.delete()

    return redirect('/rutapordefinir/') #añadr la ruta donde se vaya a redirigir

def delete_Usuario(request, usuarioid):
    usuario = Usuario.objects.get( usuario_id = usuarioid)
    usuario.delete()

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
