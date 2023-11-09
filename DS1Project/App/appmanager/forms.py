from django import forms

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
