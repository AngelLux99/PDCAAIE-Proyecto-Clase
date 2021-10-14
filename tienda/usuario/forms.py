from django import forms
from .models import Usuario, Auth

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