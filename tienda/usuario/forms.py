from django import forms
from .models import Usuario, Auth, Auth2, Producto, Factura

class RegistroForm(forms.ModelForm):

    class Meta:
        model = Usuario
        fields = ('id', 'nombre_completo','username','correo','edad', 'fotografia', 'contrasena', 'tipo_usuario')
        widgets = {
            'nombre_completo': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.TextInput(attrs={'class': 'form-control'}),
            'edad': forms.TextInput(attrs={'class': 'form-control'}),
            'fotografia': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'contrasena': forms.PasswordInput(attrs={'class': 'form-control'}),
            'tipo_usuario': forms.Select(attrs={'class': 'form-control'}),
        }

class LoginForm(forms.ModelForm):

    class Meta:
        model = Auth
        fields = ('username', 'contrasena')
        # exclude = ('nombre_completo', 'correo','edad', 'fotografia', 'tipo_usuario')

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'contrasena': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

class LoginForm2(forms.ModelForm):

    class Meta:
        model = Auth2
        fields = ('fotografia', 'username')
        # exclude = ('nombre_completo', 'correo','edad', 'fotografia', 'tipo_usuario')

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'fotografia': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class ProductoForm(forms.ModelForm):

    class Meta:
        model = Producto
        fields = ('imagen', 'nombre','descripcion','precio','cantidad')
        widgets = {
            'imagen': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.TextInput(attrs={'class': 'form-control'}),
            'cantidad': forms.TextInput(attrs={'class': 'form-control'}),
        }

class FacturaForm(forms.ModelForm):
    
    class Meta:
        model = Factura
        fields = ('nombre', 'nit','correo','direccion')
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'nit': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
        }

class RegistroFormUpdate(forms.ModelForm):

    class Meta:
        model = Usuario
        fields = ('id', 'nombre_completo','username','correo','edad', 'fotografia', 'contrasena')
        exclude = ('tipo_usuario',)
        widgets = {
            'nombre_completo': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.TextInput(attrs={'class': 'form-control'}),
            'edad': forms.TextInput(attrs={'class': 'form-control'}),
            'fotografia': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'tipo_usuario': forms.Select(attrs={'class': 'form-control'}),
            'contrasena': forms.PasswordInput(attrs={'class': 'form-control'}),
        }