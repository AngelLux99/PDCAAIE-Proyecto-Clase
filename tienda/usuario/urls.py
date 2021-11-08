from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.registro, name="registro"),
    path('login/', views.login, name="login"),
    path('login2/', views.login2, name="login2"),
    path('', views.home, name="login1"),
    path('home/', views.home, name="home"),
    path('list/', views.listaregistro, name="Lista"),
    path('delete/<int:id>/', views.eliminar, name="Eliminar"),
    path('desbloquear/<int:id>/', views.desbloquear, name="desbloquear"),
    path('bitacora/', views.bitacora, name="Bitacora"),
    path('logout/', views.logout_view, name="logout"),
    path('face_detection/detect/', views.detect, name="detector"),
    path('formProducto/', views.agregarProducto, name="AgregarProducto"),
    path('productos/', views.producto, name="Productos"),
    path('deleteproducto/<int:id>/', views.eliminarProducto, name="EliminarProducto"),
    path('store', views.store, name="store"),
    path('carrito/<int:id>/', views.agregarCarrito, name="AgregarCarrito"),
    path('micarrito/', views.Micarrito, name="MiCarrito"),
    path('quitarcarrito/<int:id>/', views.quitarCarrito, name="QuitarCarrito"),
    path('confirmarcompra/', views.compra, name="ConfirmarCompra"),
    path('reportes/', views.reporte, name="ReporteFacturas"),
    path('factura/<int:id>/', views.reporteIndividual, name="Factura"),
    path('editarperfil/<int:id>/', views.edicion, name="Editarperfil"),

     path('usuario/', views.usuarioactual, name="usuario"),
]
