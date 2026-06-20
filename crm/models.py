from django.db import models
from django.utils import timezone
from core.models import Cliente


class Oportunidad(models.Model):
    class Etapa(models.TextChoices):
        # Define las etapas posibles del pipeline usando TextChoices
        PROSPECCION = 'PRO', 'Prospección'
        PROPUESTA = 'PRP', 'Propuesta'
        NEGOCIACION = 'NEG', 'Negociación'
        GANADA = 'GAN', 'Cerrada Ganada'
        PERDIDA = 'PER', 'Cerrada Perdida'

    titulo = models.CharField(max_length=200) # Nombre descriptivo de la oportunidad
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.RESTRICT, # Impide borrar un cliente que tiene oportunidades
        related_name='oportunidades' # Permite acceder con cliente.oportunidades.all()
    )
    valor_estimado = models.DecimalField(max_digits=12, decimal_places=2) # Importe potencial de la venta
    etapa = models.CharField(
        max_length=3,
        choices=Etapa.choices, # Limita los valores a los definidos en la clase Etapa
        default=Etapa.PROSPECCION # Por defecto empieza en Prospección
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True) # Se rellena automáticamente al crear la oportunidad
    fecha_cierre = models.DateTimeField(null=True, blank=True) # Opcional, se rellena cuando se cierra la oportunidad

    def __str__(self):
        # Representación textual de la oportunidad en el panel admin
        return f"{self.titulo} - {self.cliente.nombre}"

    @property
    def dias_abierta(self):
        # Propiedad calculada, no se guarda en la BD
        if not self.fecha_creacion:
            return 0
        # Si está cerrada usa la fecha de cierre, si sigue abierta usa la fecha actual
        final = self.fecha_cierre if self.fecha_cierre else timezone.now()
        return (final - self.fecha_creacion).days

    @property
    def esta_cerrada(self):
        # Una oportunidad está cerrada si está Ganada o Perdida
        return self.etapa in (self.Etapa.GANADA, self.Etapa.PERDIDA)

    class Meta:
        verbose_name = 'Oportunidad'
        verbose_name_plural = 'Oportunidades'
        ordering = ['-fecha_creacion'] # Orden por defecto: las más recientes primero