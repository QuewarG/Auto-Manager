# Generated by Django 4.2.7 on 2023-11-21 19:55

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_per_tipo_doc', models.CharField(max_length=10)),
                ('user_numero_doc', models.CharField(max_length=20)),
                ('user_telefono', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('cargo_cod', models.AutoField(primary_key=True, serialize=False)),
                ('cargo_nombre', models.CharField(max_length=30)),
                ('cargo_descripcion', models.TextField()),
                ('cargo_vigente', models.BooleanField(default=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='CategoriaInventario',
            fields=[
                ('categoriainv', models.AutoField(primary_key=True, serialize=False)),
                ('categoriainv_nombre', models.CharField(max_length=100)),
                ('categoriainv_vigente', models.BooleanField(default=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='CotizacionReparacion',
            fields=[
                ('cotrep_cod', models.AutoField(primary_key=True, serialize=False)),
                ('cotrep_precioreparacion', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cotrep_observaciones', models.TextField()),
                ('cotrep_fecharealizada', models.DateTimeField()),
                ('cotrep_estado', models.BooleanField(default=True)),
                ('cotrep_vigente', models.BooleanField(default=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='CotizacionRepuestos',
            fields=[
                ('cotrepues_cod', models.AutoField(primary_key=True, serialize=False)),
                ('cotrepues_preciotemporal', models.IntegerField()),
                ('cotrepues_fecharealizada', models.DateTimeField()),
                ('cotrepues_estado', models.BooleanField(default=True)),
                ('cotrepues_vigente', models.BooleanField(default=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='CotizacionVehiculo',
            fields=[
                ('cotven_cod', models.AutoField(primary_key=True, serialize=False)),
                ('cotven_fecharealizada', models.DateTimeField()),
                ('cotven_estado', models.BooleanField(default=True)),
                ('cotven_vigente', models.BooleanField(default=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Inventario',
            fields=[
                ('inv_cod', models.AutoField(primary_key=True, serialize=False)),
                ('inv_nombre', models.CharField(max_length=30)),
                ('inv_descripcion', models.TextField()),
                ('inv_precioneto', models.DecimalField(decimal_places=2, max_digits=10)),
                ('inv_vigente', models.BooleanField(default=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('inv_categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appmanager.categoriainventario')),
            ],
        ),
        migrations.CreateModel(
            name='InventarioPorSucursal',
            fields=[
                ('invsus_cod', models.AutoField(primary_key=True, serialize=False)),
                ('invsus_existencias', models.IntegerField()),
                ('invsus_vigente', models.BooleanField(default=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('invsus_codigo_inventario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appmanager.inventario')),
            ],
        ),
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('rol_cod', models.AutoField(primary_key=True, serialize=False)),
                ('rol_nombre', models.CharField(max_length=50)),
                ('rol_descripcion', models.TextField(blank=True, null=True)),
                ('rol_vigente', models.BooleanField(default=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['rol_cod'],
            },
        ),
        migrations.CreateModel(
            name='Sucursal',
            fields=[
                ('sucursal_cod', models.AutoField(primary_key=True, serialize=False)),
                ('sucursal_nombre', models.CharField(max_length=50)),
                ('sucursal_ubicacion', models.CharField(max_length=100)),
                ('sucursal_vigente', models.BooleanField(default=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('sucursal_cod_gerente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='VehiculoVenta',
            fields=[
                ('vehvnt_cod', models.AutoField(primary_key=True, serialize=False)),
                ('vehvnt_placa', models.CharField(max_length=10)),
                ('vehvnt_marca', models.CharField(max_length=30)),
                ('vehvnt_color', models.CharField(max_length=30)),
                ('vehvnt_anio', models.CharField(max_length=30)),
                ('vehvnt_precioneto', models.DecimalField(decimal_places=2, max_digits=10)),
                ('vehvnt_disponible', models.BooleanField(default=True)),
                ('vehvnt_vigente', models.BooleanField(default=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('vehvnt_cod_sucursal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appmanager.sucursal')),
            ],
        ),
        migrations.CreateModel(
            name='VehiculoReparacion',
            fields=[
                ('vehrep_cod', models.AutoField(primary_key=True, serialize=False)),
                ('vehrep_placa', models.CharField(max_length=20)),
                ('vehrep_marca', models.CharField(max_length=30)),
                ('vehrep_color', models.CharField(max_length=30)),
                ('vehrep_enReparacion', models.BooleanField(default=False)),
                ('vehrep_vigente', models.BooleanField(default=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('vehrep_dueño', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RepuestoVenta',
            fields=[
                ('repvnt_cod', models.AutoField(primary_key=True, serialize=False)),
                ('repvnt_descripcion', models.TextField()),
                ('repvnt_vigente', models.BooleanField(default=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('repvnt_inventario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appmanager.inventarioporsucursal')),
            ],
        ),
        migrations.CreateModel(
            name='PersonaXCargo',
            fields=[
                ('perxcargo_cod', models.AutoField(primary_key=True, serialize=False)),
                ('perxcargo_vigente', models.BooleanField(default=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('perxcargo_cargo_cod', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appmanager.cargo')),
                ('perxcargo_persona_cod', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('perxcargo_sucursal_cod', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appmanager.sucursal')),
            ],
        ),
        migrations.CreateModel(
            name='OrdenTrabajo',
            fields=[
                ('orden_cod', models.AutoField(primary_key=True, serialize=False)),
                ('orden_observacion', models.TextField()),
                ('orden_estado', models.BooleanField(default=True)),
                ('orden_fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('orden_vigente', models.BooleanField(default=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('orden_encargado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('orden_vehiculoreparacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appmanager.vehiculoreparacion')),
            ],
        ),
        migrations.AddField(
            model_name='inventarioporsucursal',
            name='invsus_sucursal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appmanager.sucursal'),
        ),
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('codfac', models.AutoField(primary_key=True, serialize=False)),
                ('codfac_subtotal', models.DecimalField(decimal_places=2, max_digits=15)),
                ('codfac_iva', models.DecimalField(decimal_places=2, max_digits=15)),
                ('codfac_descuento', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('codfac_precioTotal', models.DecimalField(decimal_places=2, max_digits=15)),
                ('codfac_fecharealizada', models.DateField()),
                ('codfac_vigente', models.BooleanField(default=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('codfac_cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('codfac_cotizacion_vehiculonuevo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appmanager.cotizacionvehiculo')),
                ('codfac_reparacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appmanager.cotizacionreparacion')),
                ('codfac_repuestos', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appmanager.cotizacionrepuestos')),
                ('codfac_vendedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appmanager.personaxcargo')),
            ],
        ),
        migrations.AddField(
            model_name='cotizacionvehiculo',
            name='cotven_cod_vehiculo_nuevo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appmanager.vehiculoventa'),
        ),
        migrations.AddField(
            model_name='cotizacionrepuestos',
            name='cotrepues_repuestocod',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appmanager.repuestoventa'),
        ),
        migrations.AddField(
            model_name='cotizacionreparacion',
            name='cotrep_orden_trabajo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appmanager.ordentrabajo'),
        ),
        migrations.AddField(
            model_name='usuario',
            name='cod_rol',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='appmanager.rol'),
        ),
        migrations.AddField(
            model_name='usuario',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='usuario',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
