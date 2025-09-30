from django.db import models

class TipoDocumentoIdentidad(models.Model):
    idtipo_documento_identidad = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(null=True, blank=True)
    estado = models.BooleanField(default=True)

    class Meta:
        db_table = 'ad_tipo_documento_identidad'
        verbose_name = 'Tipo de Documento'
        verbose_name_plural = 'Tipos de Documento'

    def __str__(self):
        return self.nombre
