class UnidadHabitacional(models.Model):
    numero = models.CharField(max_length=10)   # Ej: "A-201"
    torre = models.CharField(max_length=50, blank=True, null=True)  # Ej: "Torre Norte"
    estado = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.torre or ''} {self.numero}".strip()