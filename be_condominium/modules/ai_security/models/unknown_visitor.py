from django.db import models

class UnknownVisitor(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='unknown_visitors/')
    face_id = models.CharField(max_length=100)
    similarity = models.FloatField()

    def __str__(self):
        return f"{self.timestamp} - {self.face_id} ({self.similarity}%)"
