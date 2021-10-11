from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.urls import reverse

# Create your views here.
def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def registro(request):
    if request.method == 'POST':
        modelform = UsuarioForm(request.POST, request.FILES) 
        print(modelform.is_valid())
        if modelform.is_valid():
            tipo = TipoUsuario.objects.get(pk=1)
            nuevo_usuario = modelform.save()
            #nuevo_usuario.tipo_usuario_id = 1
            nuevo_usuario.tipo_usuario = 1
            nuevo_usuario.intentos = 0
            nuevo_usuario.save()
            return redirect(reverse('login'))
    else:
        modelform = UsuarioForm()

    return render(request, 'registro.html', {'form': modelform})
