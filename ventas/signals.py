import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Pedido, LineaPedido

logger = logging.getLogger(__name__)


@receiver(post_save, sender=LineaPedido)
def actualizar_totales_pedido(sender, instance, **kwargs):
    """Recalcula los totales del pedido cada vez que se guarda una línea."""
    instance.pedido.calcular_totales()


@receiver(post_save, sender=Pedido)
def descontar_stock_al_confirmar(sender, instance, **kwargs):
    """Descuenta el stock de cada producto cuando el pedido se confirma."""
    if instance.estado.nombre == 'CONFIRMADO':
        lineas = instance.lineas.all()
        for linea in lineas:
            producto = linea.producto
            if producto.stock >= linea.cantidad:
                producto.stock -= linea.cantidad
                producto.save()
            else:
                logger.error(
                    f"Stock insuficiente para '{producto.nombre}'. "
                    f"Stock actual: {producto.stock}, "
                    f"cantidad pedida: {linea.cantidad}."
                )