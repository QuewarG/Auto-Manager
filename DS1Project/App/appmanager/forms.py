from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

#formulario personalizado con la tabla user para el registro de los usuarios mediante el formulario del login
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name', 'tipo_doc', 'num_doc', 'num_tel', 'rol')
        
    def clean_username(self):
        # Añade validaciones personalizadas al campo password1
        username = self.cleaned_data.get('username')

        # Ejemplo: Asegura que la contraseña tenga al menos 3 caracteres
        if len(username) >= 150:
            msg =_("Nombre de usuario muy largo.")
            raise ValidationError(msg)

        # Asegúrate de que la contraseña contenga al menos un carácter especial
        # if not any(char in "!@#$%^&*()-_=+[]{};:'\",.<>?/\\|`~" for char in username):
        #     msg = _("La contraseña debe contener al menos un carácter especial.")
        #     raise ValidationError(msg)

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


    first_name = forms.CharField(max_length=150, required=True, label='Nombre')
    last_name = forms.CharField(max_length=150, required=True, label='Apellido')
    email = forms.EmailField(required=True, help_text='Ingrese una dirección de correo valida', label='Correo Electronico')
    tipo_doc = forms.ChoiceField(choices=tipo_docs, help_text='Seleccione su tipo de documento', label='Tipo Documento')
    num_doc = forms.CharField(max_length=20, required=True, label='Numero Documento')
    num_tel = forms.CharField(max_length=20, required=False, label='Numero Telefonico')
    rol = forms.ModelChoiceField(queryset=Rol.objects.all(), empty_label=None, label='Roles disponibles')
    

class CustomUserEditForm(UserChangeForm):
    tipo_docs = [
        ('CC', 'C.C'),
        ('TI', 'T.I'),
        ('OTRO', 'OTRO'),
    ]
   
    first_name = forms.CharField(max_length=150, required=True, label='Nombre')
    last_name = forms.CharField(max_length=150, required=True, label='Apellido')
    email = forms.EmailField(required=True, help_text='Ingrese una dirección de correo valida', label='Correo Electronico')
    user_per_tipo_doc = forms.ChoiceField(choices=tipo_docs, help_text='Seleccione su tipo de documento', label='Tipo Documento')
    user_numero_doc = forms.CharField(max_length=20, required=True, label='Numero Documento')
    user_telefono = forms.CharField(max_length=20, required=False, label='Numero Telefonico')
    cod_rol = forms.ModelChoiceField (queryset=Rol.objects.all(), empty_label=None)
    
    
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'first_name', 'last_name', 'user_per_tipo_doc', 'user_numero_doc', 'user_telefono', 'cod_rol']

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            # Excluye los campos de contraseña del formulario
            self.fields.pop('password')


class RolForm(forms.ModelForm):

    class Meta:
         model = Rol
         fields = ['rol_nombre', 'rol_descripcion'] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Añadir un campo oculto y no editable
        self.fields['rol_cod'] = forms.CharField(widget=forms.HiddenInput(attrs={'readonly': 'readonly'}))

    def clean_nombre_rol(self):
        nombre_rol = self.cleaned_data['rol_nombre']

        if len(nombre_rol) < 8:
            msg = _("La contraseña debe tener al menos 8 caracteres.")
            raise ValidationError(msg)
        # Agrega las validaciones necesarias para el campo 'nombre_rol' si es necesario
        return nombre_rol
    