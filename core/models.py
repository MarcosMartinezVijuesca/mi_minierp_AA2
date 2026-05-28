from django.db import models


class Cliente(models.Model):
    nif = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=150)
    email = models.EmailField(blank=True)
    telefono = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.nombre} ({self.nif})"

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"


class Producto(models.Model):
    sku = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=150)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.nombre} ({self.sku})"

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"


class EstadoPedido(models.Model):
    ESTADOS = [
        ('BORRADOR', 'Borrador'),
        ('CONFIRMADO', 'Confirmado'),
        ('FACTURADO', 'Facturado'),
        ('COBRADO', 'Cobrado'),
    ]
    nombre = models.CharField(max_length=20, choices=ESTADOS, unique=True)

    def __str__(self):
        return self.get_nombre_display()

    class Meta:
        verbose_name = "Estado de Pedido"
        verbose_name_plural = "Estados de Pedido"