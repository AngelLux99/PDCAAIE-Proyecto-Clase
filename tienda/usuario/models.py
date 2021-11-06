from django.db import models

# Create your models here.

class TipoUsuario(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Usuario(models.Model):
    nombre_completo = models.CharField(max_length=100)
    username = models.CharField(max_length=20, unique=True)
    correo = models.EmailField()
    edad = models.IntegerField(default=0)
    fotografia = models.ImageField(upload_to='usuarios')
    contrasena = models.CharField(max_length=100)
    intentos = models.IntegerField(default=0)
    tipo_usuario = models.ForeignKey(TipoUsuario, on_delete=models.CASCADE)
    

class Auth(models.Model):
    username = models.CharField(max_length=20)
    contrasena = models.CharField(max_length=100)

class Auth2(models.Model):
    username = models.CharField(max_length=20)
    fotografia = models.ImageField(upload_to='auth')

class Bitacora(models.Model):
    direccion_ip = models.CharField(max_length=15)
    descripcion = models.CharField(max_length=500)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

class Producto(models.Model):
    imagen = models.CharField(max_length=255)
    nombre = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=1000)
    precio = models.DecimalField(max_digits=15, decimal_places=2)
    cantidad = models.IntegerField(default=0)

class Carrito(models.Model):
    cantidad = models.IntegerField(default=0)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

class Factura(models.Model):
    nombre = models.CharField(max_length=255)
    nit = models.CharField(max_length=20)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    correo = models.EmailField()
    direccion =  models.CharField(max_length=100)
    total = models.DecimalField(max_digits=15, decimal_places=2)

class DetalleFactura(models.Model):
    cantidad = models.IntegerField(default=0)
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)