import logging # Módulo de Python para registrar errores y eventos
from django.db.models.signals import post_save # Señal que se ejecuta después de guardar un objeto
from django.dispatch import receiver # Decorador para registrar funciones como receptoras de señales
from .models import Pedido, LineaPedido

logger = logging.getLogger(__name__) # Crea un logger asociado a este archivo


@receiver(post_save, sender=Pedido) # Se ejecuta automáticamente cada vez que se guarda un Pedido
def descontar_stock_al_confirmar(sender, instance, **kwargs):
    """Descuenta el stock de cada producto cuando el pedido se confirma."""
    if instance.estado.nombre.upper() == 'CONFIRMADO': # Solo actúa si el estado es CONFIRMADO
        lineas = instance.lineas.all() # Obtiene todas las líneas del pedido
        for linea in lineas: # Recorre cada línea
            producto = linea.producto # Obtiene el producto de la línea
            if producto.stock >= linea.cantidad: # Si hay stock suficiente →
                producto.stock -= linea.cantidad # ← descuenta la cantidad pedida
                producto.save() # Guarda el producto con el stock actualizado
            else:
                logger.error( # Si no hay stock suficiente → registra el error en los logs
                    f"Stock insuficiente para '{producto.nombre}'. "
                    f"Stock actual: {producto.stock}, "
                    f"cantidad pedida: {linea.cantidad}."
                )