from django.db import models
from django.db.models import CheckConstraint, Q
from core.models import Cliente, Producto, EstadoPedido
from decimal import Decimal

class Pedido(models.Model):
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.RESTRICT
    )
    estado = models.ForeignKey(
        EstadoPedido,
        on_delete=models.RESTRICT
    )
    fecha = models.DateField(auto_now_add=True)
    base = models.DecimalField(max_digits=10, decimal_places=2, default=0)      # NUEVO
    iva = models.DecimalField(max_digits=10, decimal_places=2, default=0)       # NUEVO
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)     # NUEVO

    def calcular_totales(self):
        base = sum(
            linea.precio_unitario * linea.cantidad
            for linea in self.lineas.all()
        )
        self.base = Decimal(base)
        self.iva = self.base * Decimal('0.21')
        self.total = self.base + self.iva
        self.save()

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente}"

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"


class LineaPedido(models.Model):
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name='lineas'
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.RESTRICT
    )
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad}x {self.producto} (Pedido #{self.pedido.id})"

    class Meta:
        verbose_name = "Línea de Pedido"
        verbose_name_plural = "Líneas de Pedido"
        constraints = [
            CheckConstraint(
                condition=Q(cantidad__gt=0),
                name='cantidad_positiva'
            )
        ]