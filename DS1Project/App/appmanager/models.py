from django.db import models
from django.contrib.auth.models import AbstractUser

class Rol(models.Model):
    rol_cod = models.AutoField(primary_key=True)  # SERIAL en PostgreSQL se traduce a AutoField en Django
    rol_nombre = models.CharField(max_length=50, null=False)  # NOT NULL en SQL se traduce a null=False en Django
    rol_descripcion = models.TextField(null=True, blank=True)  # Puede ser NULL en la base de datos
    rol_vigente = models.BooleanField(default=True)  # Valor predeterminado True para rol_vigente
    create_at = models.DateTimeField(auto_now_add=True)  # auto_now_add establece el valor al momento de la creación
    update_at = models.DateTimeField(auto_now=True)  # auto_now actualiza el valor cada vez que se guarda el objeto

    def __str__(self):
        return self.rol_nombre
    
    def obtener_codigo_rol(self):
        return self.rol_cod
    
    class Meta:
        ordering = ['rol_cod']

class Usuario(AbstractUser):
    user_per_tipo_doc = models.CharField(max_length=10)
    user_numero_doc = models.CharField(max_length=20)
    user_telefono = models.CharField(max_length=20)
    cod_rol = models.ForeignKey('Rol', on_delete=models.SET_DEFAULT, default=1)  # Clave foránea a rol

#MODELOS
class Cargo(models.Model):
    cargo_cod = models.AutoField(primary_key=True)  # serial en PostgreSQL se traduce a AutoField en Django
    cargo_nombre = models.CharField(max_length=30)
    cargo_descripcion = models.TextField()
    cargo_vigente = models.BooleanField(default=True)  # Valor predeterminado True para cargo_vigente
    create_at = models.DateTimeField(auto_now_add=True)  # auto_now_add establece el valor al momento de la creación
    update_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.cargo_nombre   # auto_now actualiza el valor cada vez que se guarda el objeto
    
class Sucursal(models.Model):
    sucursal_cod = models.AutoField(primary_key=True)  # serial en PostgreSQL se traduce a AutoField en Django
    sucursal_nombre = models.CharField(max_length=50)
    sucursal_ubicacion = models.CharField(max_length=100)
    sucursal_cod_gerente = models.ForeignKey('Usuario', on_delete=models.CASCADE)  # Clave foránea a la tabla Uusuario
    sucursal_vigente = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)  # auto_now_add establece el valor al momento de la creación
    update_at = models.DateTimeField(auto_now=True)  # auto_now actualiza el valor cada vez que se guarda el objeto
    
    def __str__(self):
        return self.sucursal_nombre  # Reemplaza 'nombre' con el campo adecuado que contiene el nombre de la sucursal

class PersonaXCargo(models.Model):
    perxcargo_cod = models.AutoField(primary_key=True)
    perxcargo_persona_cod = models.ForeignKey('Usuario', on_delete=models.CASCADE)
    perxcargo_cargo_cod = models.ForeignKey('Cargo', on_delete=models.CASCADE)
    perxcargo_sucursal_cod = models.ForeignKey('Sucursal', on_delete=models.CASCADE)
    perxcargo_vigente = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


class VehiculoVenta(models.Model):
    vehvnt_cod = models.AutoField(primary_key=True)  # serial en PostgreSQL se traduce a AutoField en Django
    vehvnt_placa = models.CharField(max_length=10)
    vehvnt_marca = models.CharField(max_length=30)
    vehvnt_modelo = models.CharField(max_length=30, default='Desconocido')
    vehvnt_color = models.CharField(max_length=30)
    vehvnt_anio = models.CharField(max_length=30)
    vehvnt_cod_sucursal = models.ForeignKey('Sucursal', on_delete=models.CASCADE)
    vehvnt_precioneto = models.DecimalField(max_digits=10, decimal_places=2)
    vehvnt_disponible = models.BooleanField(default=True)
    vehvnt_vigente = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)  # auto_now_add establece el valor al momento de la creación
    update_at = models.DateTimeField(auto_now=True)  # auto_now actualiza el valor cada vez que se guarda el objeto

class VehiculoReparacion(models.Model):
    vehrep_cod = models.AutoField(primary_key=True)  # serial en PostgreSQL se traduce a AutoField en Django
    vehrep_placa = models.CharField(max_length=20)
    vehrep_marca = models.CharField(max_length=30)
    vehrep_color = models.CharField(max_length=30)
    vehrep_enReparacion = models.BooleanField(default=False)
    vehrep_dueño = models.ForeignKey('Usuario', on_delete=models.CASCADE)  # Clave foránea a persona OjO
    vehrep_vigente = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)  # auto_now_add establece el valor al momento de la creación
    update_at = models.DateTimeField(auto_now=True)  # auto_now actualiza el valor cada vez que se guarda el objeto
    
    def __str__(self):
        return self.vehrep_placa


class OrdenTrabajo(models.Model):
    orden_cod = models.AutoField(primary_key=True)  # serial en PostgreSQL se traduce a AutoField en Django
    orden_vehiculoreparacion = models.ForeignKey('VehiculoReparacion', on_delete=models.CASCADE)  # Clave foránea a VehiculoReparacion
    orden_encargado = models.ForeignKey('Usuario', on_delete=models.CASCADE)  # Clave foránea a PersonaXCargo
    orden_observacion = models.TextField()
    orden_estado = models.BooleanField(default=False)
    orden_fecha_creacion = models.DateTimeField(auto_now_add=True)  # auto_now_add establece el valor al momento de la creación
    orden_vigente = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)  # auto_now_add establece el valor al momento de la creación
    update_at = models.DateTimeField(auto_now=True)  # auto_now actualiza el valor cada vez que se guarda el objeto

    class Meta:
        ordering = ['-orden_fecha_creacion']


class Inventario(models.Model):
    inv_cod = models.AutoField(primary_key=True)  # serial en PostgreSQL se traduce a AutoField en Django
    inv_nombre = models.CharField(max_length=30)
    inv_categoria = models.ForeignKey('CategoriaInventario', on_delete=models.CASCADE)
    inv_descripcion = models.TextField()
    inv_precioneto = models.DecimalField(max_digits=10, decimal_places=2)
    inv_vigente = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)  # auto_now_add establece el valor al momento de la creación
    update_at = models.DateTimeField(auto_now=True)  # auto_now actualiza el valor cada vez que se guarda el objeto

class InventarioPorSucursal(models.Model):
    invsus_cod = models.AutoField(primary_key=True)  # serial en PostgreSQL se traduce a AutoField en Django
    invsus_codigo_inventario = models.ForeignKey('Inventario', on_delete=models.CASCADE)  # Clave foránea a Inventario
    invsus_sucursal = models.ForeignKey('Sucursal', on_delete=models.CASCADE)  # Clave foránea a Sucursal
    invsus_existencias = models.IntegerField()
    invsus_vigente = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)  # auto_now_add establece el valor al momento de la creación
    update_at = models.DateTimeField(auto_now=True)  # auto_now actualiza el valor cada vez que se guarda el objeto

class CotizacionReparacion(models.Model):
    cotrep_cod = models.AutoField(primary_key=True)  # serial en PostgreSQL se traduce a AutoField en Django
    cotrep_orden_trabajo = models.ForeignKey('OrdenTrabajo', on_delete=models.CASCADE)  # Clave foránea a OrdenTrabajo
    cotrep_precioreparacion = models.DecimalField(max_digits=10, decimal_places=2)
    cotrep_observaciones = models.TextField()
    cotrep_estado = models.BooleanField(default=False)
    cotrep_vigente = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)  # auto_now_add establece el valor al momento de la creación
    update_at = models.DateTimeField(auto_now=True)  # auto_now actualiza el valor cada vez que se guarda el objeto

class RepuestoVenta(models.Model):
    repvnt_cod = models.AutoField(primary_key=True)  # SERIAL en PostgreSQL se traduce a AutoField en Django
    repvnt_inventario = models.ForeignKey('InventarioPorSucursal', on_delete=models.CASCADE)  # Clave foránea a InventarioPorSucursal
    repvnt_descripcion = models.TextField()
    repvnt_vigente = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)  # auto_now_add establece el valor al momento de la creación
    update_at = models.DateTimeField(auto_now=True)  # auto_now actualiza el valor cada vez que se guarda el objeto

class CotizacionRepuestos(models.Model):
    cotrepues_cod = models.AutoField(primary_key=True)  # serial en PostgreSQL se traduce a AutoField en Django
    cotrepues_repuestocod = models.ForeignKey('RepuestoVenta', on_delete=models.CASCADE)  # Clave foránea a RepuestoVenta
    cotrepues_preciotemporal = models.IntegerField()
    cotrepues_fecharealizada = models.DateTimeField()
    cotrepues_estado = models.BooleanField(default=False)
    cotrepues_vigente = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)  # auto_now_add establece el valor al momento de la creación
    update_at = models.DateTimeField(auto_now=True)  # auto_now actualiza el valor cada vez que se guarda el objeto

class CotizacionVehiculo(models.Model):
    cotven_cod = models.AutoField(primary_key=True)  # SERIAL en PostgreSQL se traduce a AutoField en Django
    cotven_cod_vehiculo_nuevo = models.ForeignKey('VehiculoVenta', on_delete=models.CASCADE)
    cotven_estado = models.BooleanField(default=False)
    cotven_vigente = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)  # auto_now_add establece el valor al momento de la creación
    update_at = models.DateTimeField(auto_now=True)  # auto_now actualiza el valor cada vez que se guarda el objeto

class Factura(models.Model):
    codfac = models.AutoField(primary_key=True)  # SERIAL en PostgreSQL se traduce a AutoField en Django
    codfac_cliente = models.ForeignKey('Usuario', on_delete=models.CASCADE)  # Clave foránea a Persona
    codfac_vendedor = models.ForeignKey('PersonaXCargo', on_delete=models.CASCADE)  # Clave foránea a PersonaXCargo
    codfac_cotizacion_vehiculonuevo = models.ForeignKey('CotizacionVehiculo', on_delete=models.CASCADE)  # Clave foránea a CotizacionVehiculo
    codfac_reparacion = models.ForeignKey('CotizacionReparacion', on_delete=models.CASCADE)  # Clave foránea a CotizacionReparacion
    codfac_repuestos = models.ForeignKey('CotizacionRepuestos', on_delete=models.CASCADE)  # Clave foránea a CotizacionRepuestos
    codfac_subtotal = models.DecimalField(max_digits=15, decimal_places=2)
    codfac_iva = models.DecimalField(max_digits=15, decimal_places=2)
    codfac_descuento = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    codfac_precioTotal = models.DecimalField(max_digits=15, decimal_places=2)
    codfac_fecharealizada = models.DateField()
    codfac_vigente = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)  # auto_now_add establece el valor al momento de la creación
    update_at = models.DateTimeField(auto_now=True)  # auto_now actualiza el valor cada vez que se guarda el objeto

class CategoriaInventario(models.Model):
    categoriainv = models.AutoField(primary_key=True)
    categoriainv_nombre = models.CharField(max_length=100)
    categoriainv_vigente = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)  # auto_now_add establece el valor al momento de la creación
    update_at = models.DateTimeField(auto_now=True)  # auto_now actualiza el valor cada vez que se guarda el objeto


    def __str__(self):
        return self.categoriainv_nombre
   
