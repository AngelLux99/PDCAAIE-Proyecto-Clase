from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistroForm, LoginForm
from .models import Usuario, Bitacora
import socket
import sweetify

# Create your views here.
def registro(request):
    if request.method == "POST":
        form = RegistroForm(request.POST, request.FILES)
        print(form.is_valid())
        if form.is_valid():
            form.save()
            data = form.cleaned_data
            username = data['username']
            registrar_bitacora("Usuario registrado exitosamente.", Usuario.objects.get(username=username))
            return redirect('/login')
    else:
        form = RegistroForm()

    return render(request, 'auth/registro.html', {'forms':form})

def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        print(form.is_valid())
        
        if form.is_valid():
            data = form.cleaned_data
            username = data['username']
            contrasena = data['contrasena']
            try:
                auth = Usuario.objects.get(username=username)
            except:
                auth = None
            if auth:
                if(auth.contrasena == contrasena):
                    registrar_bitacora("El usuario " + str(username) + " ha ingresado al sistema exitosamente.", auth)
                    sweetify.success(request, 'Bienvenido al sistema.')
                    return redirect('/home')
                else:
                    auth.intentos = auth.intentos + 1
                    auth.save()
                    registrar_bitacora("El usuario " + str(username) + " ha intentado ingresar al sistema.", auth)
                    sweetify.info(request, 'Usuario o contraseña incorrecto', button='Ok', timer=3000)
                    # return redirect('/')
                    return redirect('/login')
            else:
                return redirect('/login')
    else:
        form = LoginForm()

    return render(request, 'auth/login.html', {'forms_login':form})

def home(request):
    return render(request, 'auth/index.html')


def registrar_bitacora(descripcion, usuario):
    registro_bitacora = Bitacora()
    registro_bitacora.direccion_ip = socket.gethostbyname(socket.gethostname())
    registro_bitacora.descripcion = descripcion
    registro_bitacora.usuario = usuario
    registro_bitacora.save()