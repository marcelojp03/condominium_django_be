from django.db import models
from modules.ad.models.rol import Rol


class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    foto = models.CharField(max_length=255, null=True, blank=True)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.correo

    @property
    def roles(self):
        return Rol.objects.filter(usuariorol__usuario=self)