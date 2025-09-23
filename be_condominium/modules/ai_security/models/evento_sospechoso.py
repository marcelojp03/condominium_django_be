from django.db import models

class EventoSospechoso(models.Model):
    imagen = models.ImageField(upload_to='eventos_sospechosos/')
    fecha_hora = models.DateTimeField(auto_now_add=True)
    tipo_evento = models.CharField(max_length=100)  # Ej: 'perro_suelto'
    confianza = models.FloatField()
    metadatos = models.JSONField(default=dict)
