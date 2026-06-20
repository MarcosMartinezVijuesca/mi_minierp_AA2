from django.db import models
from django.db.models import CheckConstraint, Q
from core.models import Cliente, Producto, EstadoPedido
from decimal import Decimal


class Pedido(models.Model):
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.RESTRICT # Impide borrar un cliente que tiene pedidos
    )
    estado = models.ForeignKey(
        EstadoPedido,
        on_delete=models.RESTRICT # Impide borrar un estado que tiene pedidos
    )
    fecha = models.DateField(auto_now_add=True) # Se rellena automáticamente al crear el pedido
    iva_porcentaje = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal('21.00') # IVA como campo, permite cambiarlo sin tocar el código
    )
    base = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    iva = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    def calcular_totales(self):
        # Calcula base, IVA y total a partir de las líneas del pedido
        base = sum(
            (linea.total_price for linea in self.lineas.all()),
            Decimal('0.00') # Valor inicial del sum para evitar errores con decimales
        )
        self.base = base.quantize(Decimal('0.01')) # Redondea a 2 decimales
        self.iva = (self.base * (self.iva_porcentaje / Decimal('100'))).quantize(Decimal('0.01'))
        self.total = (self.base + self.iva).quantize(Decimal('0.01'))
        # Actualiza directamente en la BD sin llamar a self.save() para evitar bucles
        Pedido.objects.filter(pk=self.pk).update(
            base=self.base,
            iva=self.iva,
            total=self.total,
        )

    def __str__(self):
        # Representación textual del pedido en el panel admin
        return f"Pedido #{self.id} - {self.cliente}"

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"


class LineaPedido(models.Model):
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE, # Borra las líneas si se borra el pedido
        related_name='lineas' # Permite acceder con pedido.lineas.all()
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.RESTRICT # Impide borrar productos que tienen líneas de pedido
    )
    cantidad = models.PositiveIntegerField() # Solo acepta valores positivos
    precio_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Precio al momento de la venta" # Texto de ayuda en el formulario
        # Importante: se guarda el precio en el momento de la venta porque podría cambiar en el futuro
    )

    @property
    def total_price(self):
        # Propiedad calculada, no se guarda en la BD
        # Multiplica precio por cantidad y redondea a 2 decimales
        return (self.precio_unitario * self.cantidad).quantize(Decimal('0.01'))

    def save(self, *args, **kwargs):
        # Sobrescribe save para recalcular totales del pedido automáticamente
        super().save(*args, **kwargs) # Primero guarda la línea normalmente
        self.pedido.calcular_totales() # Luego recalcula los totales del pedido

    def delete(self, *args, **kwargs):
        # Sobrescribe delete para recalcular totales también al borrar una línea
        pedido = self.pedido # Guarda la referencia antes de borrar
        super().delete(*args, **kwargs) # Borra la línea
        pedido.calcular_totales() # Recalcula los totales del pedido

    def __str__(self):
        # Representación textual de la línea en el panel admin
        return f"{self.cantidad}x {self.producto} (Pedido #{self.pedido.id})"

    class Meta:
        verbose_name = "Línea de Pedido"
        verbose_name_plural = "Líneas de Pedido"
        constraints = [
            CheckConstraint(
                condition=Q(cantidad__gt=0), # cantidad > 0
                name='cantidad_positiva'
            )
        ]