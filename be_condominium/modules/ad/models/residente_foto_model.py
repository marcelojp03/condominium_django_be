from django.db import models
from modules.ad.models.residente_model import Residente

class ResidenteFoto(models.Model):
    idfoto = models.AutoField(primary_key=True)
    residente = models.ForeignKey(Residente, on_delete=models.CASCADE)
    url_imagen = models.TextField()
    fecha_registro = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=20, null=True, blank=True)  # 'ENTRENAMIENTO', 'VERIFICACION'
    rekognition_face_id = models.CharField(max_length=100, null=True, blank=True)  # FaceId en Rekognition
    estado = models.BooleanField(default=True)

    class Meta:
        db_table = 'ad_residente_foto'
        verbose_name = 'Foto de Residente'
        verbose_name_plural = 'Fotos de Residentes'

    def __str__(self):
        return f"Foto {self.idfoto} - {self.residente}"
