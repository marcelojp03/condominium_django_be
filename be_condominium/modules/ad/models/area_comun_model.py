from django.db import models

class AreaComun(models.Model):
    idarea = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    capacidad = models.IntegerField()
    horario_inicio = models.TimeField()
    horario_fin = models.TimeField()
    estado = models.BooleanField(default=True)

    class Meta:
        db_table = 'ad_area_comun'
        verbose_name = 'Área Común'
        verbose_name_plural = 'Áreas Comunes'

    def __str__(self):
        return self.nombre
