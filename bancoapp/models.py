from django.db import models
from django.contrib.auth.models import AbstractUser 

# Create your models here.

class Usuarios(AbstractUser):
    cedula = models.IntegerField(null=True)
    socio = models.BooleanField(default=False)

class Fondo(models.Model):
    inversionista = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    ahorro = models.IntegerField()

    def __str__(self):
        return f'{self.inversionista.username} {self.inversionista.last_name} {self.ahorro}'

class FondoBanco(models.Model):
    total = models.IntegerField()

    def __str__(self):
        return f'{self.total}'

class Prestamo(models.Model):
    prestamista = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    prestamo = models.IntegerField(null=True, default=0)
    cuotasPrestamo = models.IntegerField(null=True, default=0)
    cuotasPorPagar = models.IntegerField(null=True, default=0)
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.prestamista.username} {self.prestamista.last_name} - {self.prestamo} - {self.fecha} - {self.cuotasPrestamo}'






