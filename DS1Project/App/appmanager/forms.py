from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.fields import ReCaptchaV2Checkbox

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'id': 'username', 'required': True}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'password', 'required': True}))
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

# Formulario personalizado con la tabla user para el registro de los usuarios mediante el formulario del login
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name', 'tipo_doc', 'num_doc', 'num_tel', 'rol', 'cod_sucursal')
        
        labels ={
             'username': _('Username'),
        }
        
    def clean_username(self):
        # Añade validaciones personalizadas al campo password1
        username = self.cleaned_data.get('username')

        # Ejemplo: Asegura que la contraseña tenga al menos 3 caracteres
        if len(username) >= 150:
            msg =_("Nombre de usuario muy largo.")
            raise ValidationError(msg)
        return username

    def clean_password1(self):
        # Añade validaciones personalizadas al campo password1
        password1 = self.cleaned_data.get('password1')

        # Ejemplo: Asegura que la contraseña tenga al menos 3 caracteres
        if len(password1) < 8:
            msg =  ("La contraseña debe tener al menos 8 caracteres.")
            raise ValidationError(msg)

        # Asegúrate de que la contraseña contenga al menos un carácter especial
        if not any(char in "!@#$%^&*()-_=+[]{};:'\",.<>?/\\|`~" for char in password1):
            msg = ("La contraseña debe contener al menos un carácter especial.")
            raise ValidationError(msg)

        return password1

    def clean_password2(self):
        # Añade validaciones personalizadas al campo password2
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            msg = ("Las contraseñas no coinciden.")
            raise ValidationError(msg)

        return password2
    
    def clean_rol(self):
            rol = self.cleaned_data['rol']
            return rol.rol_cod if rol else None

    tipo_docs = [
        ('CC', 'C.C'),
        ('TI', 'T.I'),
        ('OTRO', 'OTRO'),
    ]

    first_name = forms.CharField(max_length=150, required=True, label = _('Nombre') )
    last_name = forms.CharField(max_length=150, required=True, label = _('Apellido') )
    email = forms.EmailField(required=True, help_text = _('Ingrese una dirección de correo valida'), label = _('Correo Electrónico'))
    tipo_doc = forms.ChoiceField(choices=tipo_docs, help_text = _('Seleccione su tipo de documento'), label= _('Tipo Documento'))
    num_doc = forms.CharField(max_length=20, required=True, label = _('Número Documento') )
    num_tel = forms.CharField(max_length=20, required=False, label = _('Número Telefónico') )
    rol = forms.ModelChoiceField(queryset=Rol.objects.all(), empty_label=None, label = _('Roles disponibles') )
    cod_sucursal = forms.ModelChoiceField(queryset=Sucursal.objects.all(), empty_label=None, label=_('Sucursal'))


    def __init__(self, *args, **kwargs):
        # Obtener el rol actual del usuario y establecerlo como valor inicial
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        #selecciona los roles dependiendo del usuario registrado
        if self.user and (self.user.cod_rol.rol_cod == 2 or self.user.cod_rol.rol_cod == 1):
            self.fields['rol'].queryset = Rol.objects.all()
        elif self.user and self.user.cod_rol.rol_cod == 3:
            self.fields['rol'].queryset = Rol.objects.filter(rol_cod = 5)
        else:
            self.fields['rol'].queryset = Rol.objects.none()
            
        self.fields['first_name'].label = _('Nombre')
        self.fields['last_name'].label = _('Apellido')
        self.fields['email'].label = _('Correo Electrónico')
        self.fields['tipo_doc'].label = _('Tipo Documento')
        self.fields['email'].help_text = _("Ingrese una dirección de correo valida")
        self.fields['tipo_doc'].help_text =  _('Seleccione su tipo de documento')
        self.fields['num_doc'].label = _('Número Documento')
        self.fields['num_tel'].label = _('Número Telefónico')
        self.fields['rol'].label = _("Roles disponibles")


class CustomUserEditForm(UserChangeForm):
    tipo_docs = [
        ('CC', 'C.C'),
        ('TI', 'T.I'),
        ('OTRO', 'OTRO'),
    ]
   
    first_name = forms.CharField(max_length=150, required=True, disabled=True)
    last_name = forms.CharField(max_length=150, required=True, disabled=True)
    email = forms.EmailField(required=True )
    user_per_tipo_doc = forms.ChoiceField(choices=tipo_docs )
    user_numero_doc = forms.CharField(max_length=20, required=True )
    user_telefono = forms.CharField(max_length=20, required=False )
    cod_rol = forms.ModelChoiceField (queryset=Rol.objects.all(), empty_label=None)
    cod_sucursal = forms.ModelChoiceField (queryset=Sucursal.objects.all(), empty_label=None)
    
    
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'first_name', 'last_name', 'user_per_tipo_doc', 'user_numero_doc', 'user_telefono', 'cod_rol', 'cod_sucursal']
        labels ={
             'username': _('Username'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        

        self.fields['first_name'].label = _('Nombre')
        self.fields['last_name'].label = _('Apellido')
        self.fields['email'].label = _('Correo Electrónico')
        self.fields['user_per_tipo_doc'].label = _('Tipo Documento')
        self.fields['email'].help_text = _("Ingrese una dirección de correo valida")
        self.fields['user_per_tipo_doc'].help_text =  _('Seleccione su tipo de documento')
        self.fields['user_numero_doc'].label = _('Número Documento')
        self.fields['user_telefono'].label = _('Número Telefónico')
        self.fields['cod_rol'].label = _("Cambiar Rol")
        self.fields['cod_sucursal'].label = _("Asignar sucursal")

        #SECCION DONDE SE ASIGNA LA SUCURSAL AL USUARIO
        
        # Obtener el rol actual del usuario y establecerlo como valor inicial
        usuario = kwargs.get('instance')
        
        if usuario:
            persona_cargo = PersonaXCargo.objects.filter(perxcargo_persona_cod=usuario).first()
            if persona_cargo:
                self.fields['cod_sucursal'].initial = persona_cargo.perxcargo_sucursal_cod

    def save(self, commit=True):
        user = super().save(commit=commit)

        role_to_position = {
           'Superadministrador': 'Gerente',  # Asignando el cargo de Gerente a los Superadministradores
           'Gerente': 'Gerente',
           'Vendedor': 'Vendedor',
           'Jefe de taller': 'Jefe de taller',
           'Cliente': 'Cliente'
        }
        name_position = role_to_position.get(user.cod_rol.rol_nombre, None)

        persona_cargo = PersonaXCargo.objects.filter(perxcargo_persona_cod=user).first()

        if persona_cargo:
            persona_cargo.perxcargo_sucursal_cod = self.cleaned_data.get('cod_sucursal')

            if name_position:
                cargo, created = Cargo.objects.get_or_create(cargo_nombre=name_position)
                persona_cargo.perxcargo_cargo_cod = cargo  # Actualiza el cargo del usuario en PersonaXCargo

            persona_cargo.save()
        else:
            print("Hubo un error")

        return user


class RolForm(forms.ModelForm):

    class Meta:
         model = Rol
         fields = ['rol_nombre', 'rol_descripcion'] 
         

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Añadir un campo oculto y no editable
        self.fields['rol_cod'] = forms.CharField(widget=forms.HiddenInput(attrs={'readonly': 'readonly'}))
        self.fields['rol_nombre'].label = _("Nombre del Rol")
        self.fields['rol_descripcion'].label = _("Descripción del Rol")

    def clean_nombre_rol(self):
        nombre_rol = self.cleaned_data['rol_nombre']

        if len(nombre_rol) < 8:
            msg = _("La contraseña debe tener al menos 8 caracteres.")
            raise ValidationError(msg)
        # Agrega las validaciones necesarias para el campo 'nombre_rol' si es necesario
        return nombre_rol

class SucursalForm(forms.ModelForm):
    class Meta:
        model = Sucursal
        fields = ['sucursal_nombre', 'sucursal_ubicacion', 'sucursal_cod_gerente']
        sucursal_cod_gerente = forms.ModelChoiceField( queryset=Usuario.objects.filter(cod_rol_id = 2) )


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sucursal_cod'] = forms.CharField(widget=forms.HiddenInput(attrs={'readonly': 'readonly'}))
        self.fields['sucursal_cod_gerente'].queryset = Usuario.objects.filter(cod_rol_id = 2)
        self.fields['sucursal_nombre'].label = _('Nombre sucursal')
        self.fields['sucursal_ubicacion'].label = _('Dirección de la sucursal')
        self.fields['sucursal_cod_gerente'].label = _('Gerente encargado')
        self.fields['sucursal_cod_gerente'].empty_label = None

class CrearProductoForm(forms.ModelForm):
    categoria = forms.ModelChoiceField(queryset=CategoriaInventario.objects.all(), empty_label=None)
    sucursal = forms.ModelChoiceField(queryset=Sucursal.objects.all(), empty_label=None, to_field_name='sucursal_nombre')
    existencias = forms.IntegerField()

    class Meta:
        model = Inventario
        fields = ['inv_nombre', 'inv_descripcion', 'inv_precioneto', 'categoria']
       

    def __init__(self, *args, **kwargs):
        super(CrearProductoForm, self).__init__(*args, **kwargs)
        self.fields['categoria'].label = _('Categoría')
        self.fields['inv_nombre'].label = _('Nombre')
        self.fields['inv_descripcion'].label = _('Descripción')
        self.fields['inv_precioneto'].label = _('Precio Neto')
        self.fields['sucursal'].label = _('Sucursal')
        self.fields['existencias'].label = _('Existencias')

    def save(self, commit=True):
        producto = super().save(commit=False)
        if commit:
            producto.save()

            # Obtener los datos del formulario
            sucursal = self.cleaned_data.get('sucursal')
            existencias = self.cleaned_data.get('existencias')

            # Guardar en InventarioPorSucursal
            inventario_por_sucursal, _ = InventarioPorSucursal.objects.get_or_create(
                invsus_codigo_inventario=producto,
                invsus_sucursal=sucursal,
                defaults={'invsus_existencias': existencias}
            )
            inventario_por_sucursal.invsus_existencias = existencias
            inventario_por_sucursal.save()
        return producto


class OrdenTrabajoVehiculoForm(forms.ModelForm):
    vehrep_placa = forms.CharField(max_length=20)
    vehrep_marca = forms.CharField(max_length=30)
    vehrep_color = forms.CharField(max_length=30)
    vehrep_enReparacion = forms.BooleanField(required=False)
    orden_encargado = forms.ModelChoiceField(queryset=Usuario.objects.filter(cod_rol_id = 4), empty_label=None)
    orden_dueño = forms.ModelChoiceField(queryset=Usuario.objects.filter(cod_rol_id=5), empty_label=None)

    class Meta:
        model = OrdenTrabajo
        fields = ['orden_encargado', 'orden_dueño', 'orden_observacion']

    def __init__(self, *args, **kwargs):
        super(OrdenTrabajoVehiculoForm, self).__init__(*args, **kwargs)
        self.fields['orden_encargado'].label = _('Encargado')
        self.fields['orden_dueño'].label = _('Dueño')
        self.fields['orden_observacion'].label = _('Observaciones')
        self.fields['vehrep_placa'].label = _('Placa del vehículo')
        self.fields['vehrep_marca'].label = _('Marca del vehículo')
        self.fields['vehrep_color'].label = _('Color del vehículo')
        self.fields['vehrep_enReparacion'].label = _('¿En reparación?')
    
    def save(self, commit=True):
        vehiculo_data = {
            'vehrep_placa': self.cleaned_data['vehrep_placa'],
            'vehrep_marca': self.cleaned_data['vehrep_marca'],
            'vehrep_color': self.cleaned_data['vehrep_color'],
            'vehrep_enReparacion': self.cleaned_data['vehrep_enReparacion'],
            'vehrep_dueño': self.cleaned_data['orden_dueño'],  
        }
        vehiculo = VehiculoReparacion.objects.create(**vehiculo_data)

        orden_trabajo = super().save(commit=False)
        orden_trabajo.orden_vehiculoreparacion = vehiculo
        if commit:
            orden_trabajo.save()
        return orden_trabajo
    
# !!!
class EditarOrdenTrabajoForm(forms.ModelForm):
    vehrep_placa = forms.CharField(max_length=20)
    vehrep_marca = forms.CharField(max_length=30)
    vehrep_color = forms.CharField(max_length=30)
    vehrep_enReparacion = forms.BooleanField(required=False)
    orden_encargado = forms.ModelChoiceField(queryset=Usuario.objects.filter(cod_rol_id=4), empty_label=None)
    orden_dueño = forms.ModelChoiceField(queryset=Usuario.objects.filter(cod_rol_id=5), empty_label=None)

    class Meta:
        model = OrdenTrabajo
        fields = ['orden_encargado', 'orden_dueño', 'orden_observacion', 'vehrep_placa', 'vehrep_marca', 'vehrep_color', 'vehrep_enReparacion']

    def __init__(self, *args, **kwargs):
        super(EditarOrdenTrabajoForm, self).__init__(*args, **kwargs)
        self.fields['orden_encargado'].label = _('Encargado')
        self.fields['orden_dueño'].label = _('Dueño')
        self.fields['orden_observacion'].label = _('Observaciones')
        self.fields['vehrep_placa'].label = _('Placa del vehículo')
        self.fields['vehrep_marca'].label = _('Marca del vehículo')
        self.fields['vehrep_color'].label = _('Color del vehículo')
        self.fields['vehrep_enReparacion'].label = _('¿En reparación?')

    def save(self, commit=True):
        vehiculo_data = {
            'vehrep_placa': self.cleaned_data['vehrep_placa'],
            'vehrep_marca': self.cleaned_data['vehrep_marca'],
            'vehrep_color': self.cleaned_data['vehrep_color'],
            'vehrep_enReparacion': self.cleaned_data['vehrep_enReparacion'],
            'vehrep_dueño': self.cleaned_data['orden_dueño'],
        }
        vehiculo = VehiculoReparacion.objects.create(**vehiculo_data)

        orden_trabajo = super().save(commit=False)
        orden_trabajo.orden_vehiculoreparacion = vehiculo
        if commit:
            orden_trabajo.save()
        return orden_trabajo


class CotizacionReparacionForm(forms.ModelForm):

    cotrep_orden_trabajo = forms.ModelChoiceField(queryset=OrdenTrabajo.objects.filter(orden_estado = False ), empty_label=None)

    class Meta:
        model = CotizacionReparacion
        fields = ['cotrep_orden_trabajo','cotrep_precioreparacion','cotrep_observaciones']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['cotrep_cod'] = forms.CharField(widget=forms.HiddenInput(attrs={'readonly': 'readonly'}))
        self.fields['cotrep_orden_trabajo'].widget = forms.Select(attrs={'class': 'select form-select'}, choices=self.get_choices() )
        self.fields['cotrep_orden_trabajo'].label = _('Orden de trabajo')
        self.fields['cotrep_precioreparacion'].label = _('Precio Cotizado de la Reparación')
        self.fields['cotrep_observaciones'].label = _('Observaciones')

    def get_choices(self):
        # Obtén las opciones para el widget con el formato deseado
        choices = []
        for orden in OrdenTrabajo.objects.filter(orden_estado = False ):
            vehiculo = orden.orden_vehiculoreparacion
            label = f'{orden.orden_cod} | {vehiculo.vehrep_placa} | {vehiculo.vehrep_dueño.username} | {orden.orden_fecha_creacion.strftime("%d/%m/%Y")}'
            choices.append((orden.pk, label))
        return choices
    
class VehiculoVentaForm(forms.ModelForm):
    class Meta:
        model = VehiculoVenta
        fields = ['vehvnt_placa', 'vehvnt_marca', 'vehvnt_modelo' , 'vehvnt_color', 'vehvnt_anio', 'vehvnt_cod_sucursal', 'vehvnt_precioneto', 'vehvnt_disponible', 'vehvnt_vigente']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vehvnt_placa'].label = _('Placa del Vehículo')
        self.fields['vehvnt_marca'].label = _('Marca del Vehículo')
        self.fields['vehvnt_modelo'].label = _('Modelo del Vehículo')
        self.fields['vehvnt_color'].label = _('Color del Vehículo')
        self.fields['vehvnt_anio'].label = _('Año del Vehículo')
        self.fields['vehvnt_cod_sucursal'].label = _('Sucursal del Vehículo')
        self.fields['vehvnt_precioneto'].label = _('Precio Neto del Vehículo')
        self.fields['vehvnt_disponible'].label = _('Disponibilidad del Vehículo')
        self.fields['vehvnt_vigente'].label = _('Vigencia del Vehículo')
        self.fields['vehvnt_cod_sucursal'].queryset = Sucursal.objects.filter(sucursal_vigente=True)


class EditarProductoForm(forms.ModelForm):
    categoria = forms.ModelChoiceField(queryset=CategoriaInventario.objects.all(), empty_label=None)
    sucursal = forms.ModelChoiceField(queryset=Sucursal.objects.all(), empty_label=None, to_field_name='sucursal_nombre')
    existencias = forms.IntegerField()

    class Meta:
        model = Inventario
        fields = ['inv_nombre', 'inv_descripcion', 'inv_precioneto', 'categoria']
       
    def __init__(self, *args, **kwargs):
        super(EditarProductoForm, self).__init__(*args, **kwargs)
        self.fields['categoria'].label = _('Categoría')
        self.fields['inv_nombre'].label = _('Nombre')
        self.fields['inv_descripcion'].label = _('Descripción')
        self.fields['inv_precioneto'].label = _('Precio Neto')
        self.fields['sucursal'].label = _('Sucursal')
        self.fields['existencias'].label = _('Existencias')

    def save(self, commit=True):
        producto = super().save(commit=False)
        if commit:
            producto.save()

            # Obtener los datos del formulario
            sucursal = self.cleaned_data.get('sucursal')
            existencias = self.cleaned_data.get('existencias')

            # Guardar en InventarioPorSucursal
            inventario_por_sucursal, _ = InventarioPorSucursal.objects.get_or_create(
                invsus_codigo_inventario=producto,
                invsus_sucursal=sucursal,
                defaults={'invsus_existencias': existencias}
            )
            inventario_por_sucursal.invsus_existencias = existencias
            inventario_por_sucursal.save()

        return producto
