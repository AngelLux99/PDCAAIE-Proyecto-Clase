from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.registro, name="registro"),
    path('login/', views.login, name="login"),
    path('home/', views.home, name="home"),
    path('list/', views.listaregistro, name="Lista"),
    path('delete/<int:id>/', views.eliminar, name="Eliminar"),
    path('desbloquear/<int:id>/', views.desbloquear, name="desbloquear"),
    path('bitacora/', views.bitacora, name="Bitacora"),
    
]
