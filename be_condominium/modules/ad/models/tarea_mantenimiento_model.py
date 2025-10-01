from django.db import models
from modules.ad.models.usuario import Usuario

class TareaMantenimiento(models.Model):
    idtarea = models.AutoField(primary_key=True)
    descripcion = models.TextField()
    responsable = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20)  # 'INTERNO', 'EXTERNO'
    fecha_programada = models.DateField()
    fecha_ejecucion = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=20, default='PENDIENTE')  # 'PENDIENTE', 'EN PROCESO', 'COMPLETADA'
    costo = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    observaciones = models.TextField(null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    usuario_alta = models.ForeignKey(Usuario, on_delete=models.PROTECT)

    class Meta:
        db_table = 'ad_tarea_mantenimiento'
        verbose_name = 'Tarea de Mantenimiento'
        verbose_name_plural = 'Tareas de Mantenimiento'

    def __str__(self):
        return f"{self.descripcion[:40]} ({self.estado})"
