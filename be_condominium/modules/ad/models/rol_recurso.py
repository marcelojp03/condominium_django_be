from django.db import models
from .rol import Rol
from .recurso import Recurso
from .subrecurso import Subrecurso

class RolRecurso(models.Model):
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    recurso = models.ForeignKey(Recurso, on_delete=models.CASCADE)
    subrecurso = models.ForeignKey(Subrecurso, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('rol', 'recurso', 'subrecurso')

    def __str__(self):
        return f"{self.rol.nombre} - {self.recurso.nombre} - {self.subrecurso.nombre}"
