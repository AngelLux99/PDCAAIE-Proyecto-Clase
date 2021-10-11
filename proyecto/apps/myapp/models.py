from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings

# Create your models here.
class TimeStampModel(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class TipoUsuario(models.Model):
    nombre = models.CharField(max_length=50)
    slug = models.SlugField(editable=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.nombre)
        super(TipoUsuario, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre

class Usuario(models.Model):
    nombre_completo = models.CharField(max_length=100)
    slug = models.SlugField(editable=False)
    username = models.CharField(max_length=20, unique=True)
    correo = models.EmailField()
    edad = models.IntegerField(default=0)
    fotografia = models.ImageField(upload_to='usuarios')
    contrasena = models.CharField(max_length=100)
    intentos = models.IntegerField(default=0)
    tipo_usuario = models.ForeignKey(TipoUsuario, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.username)
        super(Usuario, self).save(*args, **kwargs)

    def __str__(self):
        return self.username

class Bitacora(TimeStampModel):
    direccion_ip = models.CharField(max_length=15)
    slug = models.SlugField(editable=False)
    descripcion = models.CharField(max_length=500)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.direccion_ip)
        super(Bitacora, self).save(*args, **kwargs)

    def __str__(self):
        return self.direccion_ip
