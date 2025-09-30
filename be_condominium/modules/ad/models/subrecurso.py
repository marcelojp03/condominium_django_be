from django.db import models
from .recurso import Recurso

class Subrecurso(models.Model):
    recurso = models.ForeignKey(Recurso, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200, null=True, blank=True)
    url = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.recurso.nombre} - {self.nombre}"
