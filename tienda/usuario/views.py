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
            messages.add_message(request, level=messages.SUCCESS, message="Usuario Registrado con Exito")
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
                if(auth.intentos<6):
                    if(auth.contrasena == contrasena):
                        registrar_bitacora("El usuario " + str(username) + " ha ingresado al sistema exitosamente.", auth)
                        sweetify.success(request, 'Bienvenido al sistema.')
                        auth.intentos = 0
                        auth.save()
                        return redirect('/home')
                    else:
                        auth.intentos = auth.intentos + 1
                        auth.save()
                        registrar_bitacora("El usuario " + str(username) + " ha intentado ingresar al sistema.", auth)
                        
                        messages.add_message(request, level=messages.SUCCESS, message="Usuario o Contraseña incorrecta")
                        if(auth.intentos == 3):
                            #Motrar mensaje de advertencia
                            messages.add_message(request, level=messages.SUCCESS, message="ADVERTENCIA: actualmente lleva 3 intentos para ingresar, a los 6 se bloqueara su usuario")
                            return redirect('/login')
                           
                        if(auth.intentos == 6):
                            messages.add_message(request, level=messages.SUCCESS, message="Ha llegado al limite de intentos. Se ha bloqueado su usuario")
                            registrar_bitacora("El usuario " + str(username) + " esta bloqueado actualmente.", auth)
                            return redirect('/login')
                            
                        # return redirect('/')
                else:
                    messages.add_message(request, level=messages.SUCCESS, message="USUARIO BLOQUEADO: Consulte con un usuario administrador para poder desbloquear su usuario")
                    return redirect('/login')
                    
            else:
    
                return redirect('/login')
    else:
        form = LoginForm()

    return render(request, 'auth/login.html', {'forms_login':form})

def listaregistro(request):
    context = {'lista_registros' : Usuario.objects.all()}
    return render(request, 'auth/listaregistro.html', context)

def eliminar(request, id):
    Usuario2 = Usuario.objects.get(pk=id)
    Usuario2.delete()
    return redirect('/list')

def desbloquear(request, id):
    Usuario2 = Usuario.objects.get(pk=id)
    Usuario2.intentos = 0
    Usuario2.save()
    #registrar_bitacora("Se ha desbloqueado el usuario " + str(username), Usuario.objects.get(username=username))
    return redirect('/list')

def bitacora(request):
    context2 = {'bitacora' : Bitacora.objects.all()}
    return render(request, 'auth/bitacora.html', context2)

def home(request):
    return render(request, 'auth/index.html')


def registrar_bitacora(descripcion, usuario):
    registro_bitacora = Bitacora()
    registro_bitacora.direccion_ip = socket.gethostbyname(socket.gethostname())
    registro_bitacora.descripcion = descripcion
    registro_bitacora.usuario = usuario
    registro_bitacora.save()