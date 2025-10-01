from django.db import models

class Rol(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=100, unique=True, null=True, blank=True)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
