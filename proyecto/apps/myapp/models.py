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

    def save(self, *arg, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(TipoUsuario, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

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

    def save(self, *arg, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(Usuario, self).save(*args, **kwargs)

    def __str__(self):
        return self.username

class Bitacora(TimeStampModel):
    direccion_ip = models.CharField(max_length=15)
    slug = models.SlugField(editable=False)
    descripcion = models.CharField(max_length=500)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def save(self, *arg, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(Bitacora, self).save(*args, **kwargs)

    def __str__(self):
        return self.direccion_ip

""" class UserManager(AbstractBaseUser, models.Manager):

    def _create_user(self, nombre_completo, username, correo, edad, fotografia, contrasena, intentos, tipoUsuarioId):

        correo = self.normalize_correo(correo)
        if not (correo):
            raise ValueError('El correo es obligatorio')
        user = self.model(nombre_completo= nombre_completo, username = username, correo = correo, edad = edad, fotografia=fotografia, contrasena=contrasena,  intentos =  intentos, tipoUsuarioId = tipoUsuarioId)
        user.set_password(contrasena)
        user.save(using = self._db)
        return user

    def create_user(self, nombre_completo, username, correo, edad, fotografia, contrasena, intentos, tipoUsuarioId):
        return self._create_user(self, nombre_completo, username, correo, edad, fotografia, contrasena, intentos, tipoUsuarioId)



class Usuarios(AbstractBaseUser,PermissionsMixin):

    nombre_completo = models.CharField(max_length=100)
    username = models.CharField(max_length=20)
    correo = models.EmailField()
    edad = models.IntegerField(max_digits=2, default=0)
    fotografia = models.CharField(max_length=100)
    contrasena = models.CharField(max_length=100)
    intentos = models.IntegerField(default=0)
    tipoUsuarioId = models.IntegerField()

    objects = UserManager()

    slug = models.SlugField(editable=False)

    def save(self, *args, **kwargs):
         if not self.id: 
             self.slug = slugify(self.name)
    super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre_completo

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['nombre_completo','username','correo','edad','fotografia','contrasena','intentos','tipoUsuario']
    
    def get_short_name(self):
        return self.username

class TipoUsuarios(models.Model):

    nombre = models.CharField(max_length=50)
    slug = models.SlugField(editable=False)

    def save(self, *args, **kwargs):
         if not self.id: 
             self.slug = slugify(self.name)
    super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre


 """