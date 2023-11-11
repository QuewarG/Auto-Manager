from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *


class create_Rol(forms.Form):
    rol_nombre = forms.CharField(label = 'Nombre', max_length = 50)
    rol_descripcion = forms.CharField(label = 'Descripción', max_length = 100)


class create_User(forms.Form):
    usuario_nickname = forms.CharField(label = 'Nombre', max_length = 20)
    usuario_correo = forms.EmailField(label = 'Correo', max_length = 40)
    usuario_password = forms.CharField(label = 'Contraseña', max_length = 20, widget = forms.PasswordInput)
    """roles = (
        ('Vendedor', 'Vendedor'),
        ('Mecanico', 'Mecanico'),
        ('3', '3'),
        widget=forms.RadioSelect
    )"""
    usuario_rol = forms.ChoiceField(label = 'Rol')

#formulario personalizado con la tabla user para el registro de los usuarios mediante el formulario del login
class CustomUserCreationForm(UserCreationForm):
    
    tipo_docs = [
        ('CC', 'C.C'),
        ('TI', 'T.I'),
        ('OTRO', 'OTRO'),
    ]
    # Recupera todos los roles de la base de datos
    roles = Rol.objects.all()

    # Crea una lista de tuplas para las opciones del ChoiceField
    opciones_roles = [(rol.rol_cod, rol.rol_nombre) for rol in roles]
        
    
   
    first_name = forms.CharField(max_length=150, required=True, label='Nombre')
    last_name = forms.CharField(max_length=150, required=True, label='Apellido')
    email = forms.EmailField(required=True, help_text='Ingrese una dirección de correo valida', label='Correo Electronico')
    tipo_doc = forms.ChoiceField(choices=tipo_docs, help_text='Seleccione su tipo de documento', label='Tipo Documento')
    num_doc = forms.CharField(max_length=20, required=True, label='Numero Documento')
    num_tel = forms.CharField(max_length=20, required=True, label='Numero Telefonico')
    rol = forms.ChoiceField(choices=opciones_roles, help_text='Seleccione El usuario a asignar', label='Usuarios disponibles')
    
    
    class Meta:
        model = Usuario
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name', 'tipo_doc', 'num_doc', 'num_tel', 'rol')



