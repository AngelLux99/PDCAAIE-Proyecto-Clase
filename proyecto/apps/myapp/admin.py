from django.contrib import admin
from .models import TipoUsuario
from .models import Usuario
from .models import Bitacora

# Register your models here.
admin.site.register(TipoUsuario)
admin.site.register(Usuario)
admin.site.register(Bitacora)

class Useradmin(admin.ModelAdmin):
    fieldsets = (
        ('User', {}),
        

    ) 
