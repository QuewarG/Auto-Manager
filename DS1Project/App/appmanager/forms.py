from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *


class create_Rol(forms.Form):
    rol_nombre = forms.CharField(label = 'Nombre', max_length = 50)
    rol_descripcion = forms.CharField(label = 'Descripción', max_length = 100)

#formulario personalizado con la tabla user para el registro de los usuarios mediante el formulario del login
class CustomUserCreationForm(UserCreationForm):
    
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
    
    
    class Meta:
        model = Usuario
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name', 'tipo_doc', 'num_doc', 'num_tel', 'rol')


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