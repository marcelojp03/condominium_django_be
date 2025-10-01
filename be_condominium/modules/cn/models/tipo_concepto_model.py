from django.db import models

class TipoConcepto(models.Model):
    idtipo_concepto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(null=True, blank=True)
    estado = models.BooleanField(default=True)

    class Meta:
        db_table = 'cn_tipo_concepto'
        verbose_name = 'Tipo de Concepto'
        verbose_name_plural = 'Tipos de Concepto'

    def __str__(self):
        return self.nombre
