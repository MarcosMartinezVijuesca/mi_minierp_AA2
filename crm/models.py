from django.db import models
from core.models import Cliente


class Oportunidad(models.Model):
    ETAPAS = [
        ('PROSPECCION', 'Prospección'),
        ('PROPUESTA', 'Propuesta'),
        ('NEGOCIACION', 'Negociación'),
        ('CERRADA_GANADA', 'Cerrada Ganada'),
        ('CERRADA_PERDIDA', 'Cerrada Perdida'),
    ]

    titulo = models.CharField(max_length=200)
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.RESTRICT
    )
    valor_estimado = models.DecimalField(max_digits=10, decimal_places=2)
    etapa = models.CharField(max_length=20, choices=ETAPAS)
    fecha_cierre = models.DateField()

    def __str__(self):
        return f"{self.titulo} - {self.get_etapa_display()}"

    class Meta:
        verbose_name = "Oportunidad"
        verbose_name_plural = "Oportunidades"