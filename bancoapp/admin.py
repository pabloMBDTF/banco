from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Usuarios)
admin.site.register(models.Fondo)
admin.site.register(models.Prestamo)
admin.site.register(models.FondoBanco)




