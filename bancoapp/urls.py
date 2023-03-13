from django.urls import path
from bancoapp.views import *
from django.contrib.auth import logout

urlpatterns = [
    path("home", index.as_view(), name="index"),
    path("registro", registro.as_view(), name="registro-usuario"),
    path("actualizar/<pk>", actualizar.as_view(), name="actualizar-usuario"),
    path("eliminar/<pk>", eliminar.as_view(), name="eliminar-usuario"),
    path("informacion/<int:id>", informacion, name="informacion-usuario"),
    path("fondo/<pk>", InvertirFondo.as_view(), name="fondo"),
    path("prestamo/<int:id>", DarPrestamo, name="prestamo"),
    path('logout/', logout_view, name='logout'),
    path('', login_view, name='login'),

]