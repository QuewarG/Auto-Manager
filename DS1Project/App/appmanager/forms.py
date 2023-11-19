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

#formulario personalizado con la tabla user para el registro de los usuarios mediante el formulario del login
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name', 'tipo_doc', 'num_doc', 'num_tel', 'rol')
        
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
            msg = _("La contraseña debe tener al menos 8 caracteres.")
            raise ValidationError(msg)

        # Asegúrate de que la contraseña contenga al menos un carácter especial
        if not any(char in "!@#$%^&*()-_=+[]{};:'\",.<>?/\\|`~" for char in password1):
            msg = _("La contraseña debe contener al menos un carácter especial.")
            raise ValidationError(msg)

        return password1

    def clean_password2(self):
        # Añade validaciones personalizadas al campo password2
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            msg =_("Las contraseñas no coinciden.")
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
   
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True )
    email = forms.EmailField(required=True )
    user_per_tipo_doc = forms.ChoiceField(choices=tipo_docs )
    user_Número_doc = forms.CharField(max_length=20, required=True )
    user_telefono = forms.CharField(max_length=20, required=False )
    cod_rol = forms.ModelChoiceField (queryset=Rol.objects.all(), empty_label=None)
    
    
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'first_name', 'last_name', 'user_per_tipo_doc', 'user_Número_doc', 'user_telefono', 'cod_rol']
        labels ={
             'username': _('Username'),
        }

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            # Excluye los campos de contraseña del formulario
            self.fields.pop('password')

            self.fields['first_name'].label = _('Nombre')
            self.fields['last_name'].label = _('Apellido')
            self.fields['email'].label = _('Correo Electrónico')
            self.fields['user_per_tipo_doc'].label = _('Tipo Documento')
            self.fields['email'].help_text = _("Ingrese una dirección de correo valida")
            self.fields['user_per_tipo_doc'].help_text =  _('Seleccione su tipo de documento')
            self.fields['user_Número_doc'].label = _('Número Documento')
            self.fields['user_telefono'].label = _('Número Telefónico')
            self.fields['cod_rol'].label = _("Cambiar Rol")


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
        fields = ['sucursal_nombre', 'sucursal_ubicacion', 'sucursal_cod_gerente', 'sucursal_vigente']

    def __init__(self, *args, **kwargs):
        super(SucursalForm, self).__init__(*args, **kwargs)
        
        # Obtén los IDs de los roles de superadministrador y gerente
        roles_permitidos = Cargo.objects.filter(cargo_nombre__in=['Superadministrador', 'Gerente']).values_list('cargo_cod', flat=True)
        
        # Filtra los usuarios que tienen roles de superadministrador o gerente
        usuarios_permitidos = Usuario.objects.filter(cod_rol__in=roles_permitidos)
        
        # Crea una lista de tuplas con los ID y nombres de usuarios para usar en la lista desplegable
        choices = [(usuario.id, usuario.username) for usuario in usuarios_permitidos]
        
        # Asigna las opciones al campo de selección de usuarios
        self.fields['sucursal_cod_gerente'].choices = choices