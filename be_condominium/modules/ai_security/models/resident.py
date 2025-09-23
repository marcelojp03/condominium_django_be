from django.db import models

class Resident(models.Model):
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=20)
    reference_image = models.ImageField(upload_to='residents/')
    rekognition_face_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.unit})"
