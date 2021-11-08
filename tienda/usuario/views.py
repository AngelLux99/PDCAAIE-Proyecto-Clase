from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from localStoragePy import localStoragePy 
from .forms import *
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import urllib.request # python 3
import json
import cv2
import os
import numpy as np
import socket
import sweetify
import re

#Face detector
FACE_DETECTOR_PATH = "{base_path}\cascades\haarcascade_frontalface_default.xml".format(
	base_path=os.path.abspath(os.path.dirname(__file__)))
print("ACA", FACE_DETECTOR_PATH)
#BOTO 3 RECONOCIMIENTO
import boto3
#BASE 64 RECONOCIMIENTO
import base64

localStorage = localStoragePy('usuario', 'json')
# REGISTRO DE USUARIO
def registro(request):
    if request.method == "POST":
        form = RegistroForm(request.POST, request.FILES)
        print(form.is_valid())
        if form.is_valid():
            data = form.cleaned_data
            contrasena = data['contrasena']
            pattern = r"^(?=.*\d)(?=.*[\u0021-\u002b\u003c-\u0040])(?=.*[A-Z])(?=.*[a-z])\S{12,16}$"
            if re.match(pattern, contrasena):
                form.save()
                username = data['username']
                registrar_bitacora("Usuario registrado exitosamente.", Usuario.objects.get(username=username))
                messages.add_message(request, level=messages.SUCCESS, message="Usuario Registrado con Exito")
                return redirect('/login')
            else: 
                messages.add_message(request, level=messages.ERROR, message="La contraseña no es válida")
                return redirect('/registro')
    else:
        form = RegistroForm()

    return render(request, 'auth/registro.html', {'forms':form})



##### LOGIN #####
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
                        #usuario_usuario = authenticate(username=auth.username, contrasena=auth.contrasena)
                        #print(usuario_usuario)
                        auth.intentos = 0
                        auth.save()
                        localStorage.setItem('UsuarioId', auth.id)
                        localStorage.setItem('Usuario', auth.username)
                        print(localStorage.getItem("Usuario"))
                        localStorage.setItem("TipoUsuario", auth.tipo_usuario_id)
                        #print(localStorage.getItem("TipoUsuario")) 

                        if(auth.tipo_usuario_id == 1):
                            return redirect('/list')
                        if(auth.tipo_usuario_id == 2):
                            return redirect('/productos')
                        if(auth.tipo_usuario_id == 3):
                            return redirect('/reportes')
                        else:    
                            return redirect('/home')
                    else:
                        print("usuario incorrecto")
                        auth.intentos = auth.intentos + 1
                        auth.save()
                        registrar_bitacora("El usuario " + str(username) + " ha intentado ingresar al sistema.", auth)
                        
                        messages.add_message(request, level=messages.ERROR, message="Contraseña incorrecta")
                        if(auth.intentos < 3):
                            return redirect('/login')
                        if(auth.intentos == 3):
                            #Motrar mensaje de advertencia
                            messages.add_message(request, level=messages.WARNING, message="ADVERTENCIA: actualmente lleva 3 intentos para ingresar, a los 6 se bloqueara su usuario")
                            return redirect('/login')
                           
                        if(auth.intentos == 6):
                            messages.add_message(request, level=messages.ERROR, message="Ha llegado al limite de intentos. Se ha bloqueado su usuario")
                            registrar_bitacora("El usuario " + str(username) + " esta bloqueado actualmente.", auth)
                            return redirect('/login')
                            
                        # return redirect('/')
                else:
                    form = LoginForm()
                    messages.add_message(request, level=messages.ERROR, message="USUARIO BLOQUEADO: Consulte con un usuario administrador para poder desbloquear su usuario")
                    return redirect('/login')
                    
            else:
                form = LoginForm()
                messages.add_message(request, level=messages.SUCCESS, message="Usuario incorrecto")
                return redirect('/login')
    else:
        form = LoginForm()
        
    return render(request, 'auth/login.html', {'forms_login':form})

def login2(request):
    if request.method == "POST":
        form = LoginForm2(request.POST)
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
                        return redirect('/login')
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
        form = LoginForm2()
        data = form.cleaned_data
        return render(request, 'auth/login2.html', {'forms_login':form})

def logout_view(request):
    #logout(request)
    localStorage.getItem("TipoUsuario")
    localStorage.removeItem("TipoUsuario")
    usuarioId = localStorage.getItem("UsuarioId")
    usuario = Usuario.objects.get(pk=usuarioId)
    registrar_bitacora("El usuario " + str(usuario.username) + " ha salido del sistema.", usuario)
    return redirect('/login')

##### EDICIÓN DE PERFIL #####
def usuarioactual(request):
    id2=localStorage.getItem("UsuarioId")
    UsuarioA = {'UsuarioActual' : Usuario.objects.filter(pk=id2).first()}
    return render(request, 'auth/adminhome.html', UsuarioA)

def edicion(request, id):
    if request.method == "POST":
        id2=localStorage.getItem("UsuarioId")
        Usuario2 = Usuario.objects.filter(pk=id2).first()
        form = RegistroFormUpdate(request.POST, request.FILES, instance=Usuario2)
        print(form.is_valid())
        if form.is_valid():
            data = form.cleaned_data
            contrasena = data['contrasena']
            pattern = r"^(?=.*\d)(?=.*[\u0021-\u002b\u003c-\u0040])(?=.*[A-Z])(?=.*[a-z])\S{12,16}$"
            if re.match(pattern, contrasena):
                form.save()
                username = data['username']
                registrar_bitacora("Usuario registrado exitosamente.", Usuario.objects.get(username=username))
                messages.add_message(request, level=messages.SUCCESS, message="Información Actualizada con Exito")
                return redirect('/editarperfil/' + id2)
            else: 
                messages.add_message(request, level=messages.ERROR, message="La contraseña no es válida")
                return redirect('editarperfil/' + id2)
    else:
        id2=localStorage.getItem("UsuarioId")
        Usuario2 = Usuario.objects.filter(pk=id2).first()
        form = RegistroFormUpdate(instance=Usuario2)
    return render(request, 'auth/editarperfil.html', {'forms':form, 'Usuario':Usuario2})

##### FUNCIONES DE USUARIO ADMINISTRADOR #####     

def listaregistro(request):
    idUsuario = localStorage.getItem("UsuarioId")
    context = {'lista_registros' : Usuario.objects.all(), 'UsuarioActual' : Usuario.objects.filter(pk=idUsuario).first()}
    print(localStorage.getItem("TipoUsuario")) 
    TipoUsuario = localStorage.getItem("TipoUsuario")
    if(TipoUsuario == "1"):
        return render(request, 'auth/listaregistro.html', context)
    else:
        return redirect('/login')
    
    
def eliminar(request, id):
    usuarioId = localStorage.getItem("UsuarioId")
    usuario = Usuario.objects.get(pk=usuarioId)
    TipoUsuario = localStorage.getItem("TipoUsuario")
    if(TipoUsuario == "1"):
        Usuario2 = Usuario.objects.get(pk=id)
        Usuario2.delete()
        registrar_bitacora("El usuario " + str(usuario.username) + " ha eliminado al usuario " + Usuario2.username, usuario)
        messages.add_message(request, level=messages.SUCCESS, message="El Usuario se ha eliminado")
        return redirect('/list')
    else:
        return redirect('/login')

def desbloquear(request, id):
    Usuario2 = Usuario.objects.get(pk=id)
    Usuario2.intentos = 0
    Usuario2.save()
    messages.add_message(request, level=messages.SUCCESS, message="El Usuario se ha desbloqueado")
    #registrar_bitacora("Se ha desbloqueado el usuario " + str(username), Usuario.objects.get(username=username))
    return redirect('/list')

def bitacora(request):
    idUsuario = localStorage.getItem("UsuarioId")
    context2 = {'bitacora' : Bitacora.objects.all(), 'UsuarioActual' : Usuario.objects.filter(pk=idUsuario).first()}
    print(localStorage.getItem("TipoUsuario")) 
    TipoUsuario = localStorage.getItem("TipoUsuario")
    if(TipoUsuario == "1"):
        return render(request, 'auth/bitacora.html', context2)
    else:
        return redirect('/login')

def home(request):
    return render(request, 'auth/index.html')


def registrar_bitacora(descripcion, usuario):
    registro_bitacora = Bitacora()
    registro_bitacora.direccion_ip = socket.gethostbyname(socket.gethostname())
    registro_bitacora.descripcion = descripcion
    registro_bitacora.usuario = usuario
    registro_bitacora.save()

##### DETECCIÓN FACIAL #####

@csrf_exempt
def detect(request):
	# initialize the data dictionary to be returned by the request
	data = {"success": False}
	# check to see if this is a post request
	if request.method == "POST":
		# check to see if an image was uploaded
		if request.FILES.get("image", None) is not None:
			# grab the uploaded image
			image = _grab_image(stream=request.FILES["image"])
		# otherwise, assume that a URL was passed in
		else:
			# grab the URL from the request
			url = request.POST.get("url", None)
			# if the URL is None, then return an error
			if url is None:
				data["error"] = "No URL provided."
				return JsonResponse(data)
			# load the image and convert
			image = _grab_image(url=url)
		# convert the image to grayscale, load the face cascade detector,
		# and detect faces in the image
		image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		detector = cv2.CascadeClassifier(FACE_DETECTOR_PATH)
		rects = detector.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5,
			minSize=(30, 30), flags = cv2.CASCADE_SCALE_IMAGE)
		# construct a list of bounding boxes from the detection
		rects = [(int(x), int(y), int(x + w), int(y + h)) for (x, y, w, h) in rects]
		# update the data dictionary with the faces detected
		data.update({"num_faces": len(rects), "faces": rects, "success": True})
	# return a JSON response
	return JsonResponse(data)

def _grab_image(path=None, stream=None, url=None):
	# if the path is not None, then load the image from disk
	if path is not None:
		image = cv2.imread(path)
	# otherwise, the image does not reside on disk
	else:	
		# if the URL is not None, then download the image
		if url is not None:
			resp = urllib.request.urlopen(url)
			data = resp.read()
		# if the stream is not None, then the image has been uploaded
		elif stream is not None:
			data = stream.read()
		# convert the image to a NumPy array and then read it into
		# OpenCV format
		image = np.asarray(bytearray(data), dtype="uint8")
		image = cv2.imdecode(image, cv2.IMREAD_COLOR)
 
	# return the image
	return image

##### FUNCIONES DE VENDEDOR #####
def agregarProducto(request):
    idUsuario = localStorage.getItem("UsuarioId")
    TipoUsuario = localStorage.getItem("TipoUsuario")
    usuario = Usuario.objects.get(pk=idUsuario)
    if(TipoUsuario == "2"):
        if request.method == "POST":
            form = ProductoForm(request.POST, request.FILES)
            print(form.is_valid())
            if form.is_valid():
                form.save()
                data = form.cleaned_data
                #username = data['username']
                registrar_bitacora("Producto " + data['nombre'] + " registrado por el usuario: " + usuario.username, usuario)
                messages.add_message(request, level=messages.SUCCESS, message="Producto Registrado con Exito")
                return redirect('/productos')
        else:
            form = ProductoForm()

        return render(request, 'auth/formProducto.html', {'forms':form, 'UsuarioActual' : Usuario.objects.filter(pk=idUsuario).first()})
    else:
        return redirect('/login')

    
def producto(request):
    idUsuario = localStorage.getItem("UsuarioId")
    context3 = {'producto' : Producto.objects.all(), 'UsuarioActual' : Usuario.objects.filter(pk=idUsuario).first()}
    TipoUsuario = localStorage.getItem("TipoUsuario")
    if(TipoUsuario == "2"):
        return render(request, 'auth/Productos.html', context3)
    else:
        return redirect('/login')

def eliminarProducto(request, id):
    usuarioId = localStorage.getItem("UsuarioId")
    usuario = Usuario.objects.get(pk=usuarioId)
    
    TipoUsuario = localStorage.getItem("TipoUsuario")
    if(TipoUsuario == "2"):
        Producto2 = Producto.objects.get(pk=id)
        Producto2.delete()
        registrar_bitacora("El usuario " + str(usuario.username) + " ha eliminado el producto " + Producto2.nombre, usuario)
        messages.add_message(request, level=messages.SUCCESS, message="Se ha eliminado el Producto")
        return redirect('/productos')
    else:
        return redirect('/login')
    
##### FUNCIONES DE CLIENTE #####
def store(request):
    context3 = {'producto' : Producto.objects.all()}
    return render(request, 'auth/store.html', context3)

def agregarCarrito(request, id):
    Producto2 = Producto.objects.get(pk=id)
    cart = Carrito()
    cart.cantidad = 1
    cart.producto = Producto2
    cart.save()
    # RESTAR AL STOCK DE PRODUCTO
    Producto2.cantidad = Producto2.cantidad - 1
    Producto2.save()
    return redirect('/store')

def Micarrito(request):
    carrito = Carrito.objects.all()
    total = 0
    for item in carrito:
        total += item.producto.precio
    
    context3 = {'carrito' : carrito, 'total': total}
    return render(request, 'auth/Micarrito.html', context3)

def quitarCarrito(request, id):
    cart = Carrito.objects.get(pk=id)
    cart.delete()
    Producto2 = Producto.objects.get(pk=cart.producto.id)
    Producto2.cantidad = Producto2.cantidad + 1
    Producto2.save()
    return redirect('/micarrito')

def compra(request):
    carrito = Carrito.objects.all()
    total = 0
    for item in carrito:
        total += item.producto.precio
    print(request.method)
    if request.method == "POST":
        form = FacturaForm(request.POST)
        if form.is_valid():
            factura = Factura()
            factura.nombre = form.cleaned_data['nombre']
            factura.nit = form.cleaned_data['nit']
            factura.correo = form.cleaned_data['correo']
            factura.direccion = form.cleaned_data['direccion']
            factura.total = total
            factura.save()
            idFactura = Factura.objects.last()
            for item in carrito:
                detalleFactura = DetalleFactura()
                detalleFactura.cantidad = 1
                detalleFactura.factura = idFactura
                detalleFactura.producto = item.producto
                detalleFactura.save()
            Carrito.objects.all().delete()
            return redirect('/home')
        """ if form.is_valid():
            form.save()
            idFactura = Factura.objects.last()
            for item in carrito:
                detalleFactura = DetalleFactura()
                detalleFactura.cantidad = 1
                detalleFactura.factura = idFactura
                detalleFactura.producto = item.producto
                detalleFactura.save()
            Carrito.objects.all().delete()
            return redirect('/home') """
    else:
        form = FacturaForm(initial={'total': total})
    return render(request, 'auth/Compra.html', {'forms':form, 'carrito':carrito, 'total': total })

##### FUNCIONES DE REPORTES #####

def reporte(request):
    idUsuario = localStorage.getItem("UsuarioId")
    context2 = {'reporte' : Factura.objects.all(), 'UsuarioActual' : Usuario.objects.filter(pk=idUsuario).first()}
    TipoUsuario = localStorage.getItem("TipoUsuario")
    if(TipoUsuario == "3"):
        return render(request, 'auth/reporte.html', context2)
    else:
        return redirect('/login') 
    
def reporteIndividual(request, id):
    TipoUsuario = localStorage.getItem("TipoUsuario")
    if(TipoUsuario == "3"):
        factura = Factura.objects.get(pk=id)
        detalleFactura = DetalleFactura.objects.all().filter(factura=factura)
        total = 0
        for item in detalleFactura:
            total += item.producto.precio
        context2 = {'factura' : factura, 'detalle': detalleFactura, 'total': total}
        return render(request, 'auth/Factura.html', context2)
    else:
        return redirect('/login') 
    