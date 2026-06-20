from django.contrib import admin
from .models import Pedido, LineaPedido


class LineaPedidoInline(admin.TabularInline):
    # Permite editar líneas de pedido directamente dentro del pedido
    model = LineaPedido # Modelo hijo (las líneas)
    extra = 1 # Filas vacías que aparecen por defecto para añadir líneas nuevas


@admin.register(Pedido) # Registra el modelo Pedido en el panel de admin
class PedidoAdmin(admin.ModelAdmin):
    inlines = [LineaPedidoInline] # Conecta las líneas con el pedido
    list_display = ('id', 'cliente', 'fecha', 'estado', 'base', 'iva', 'total') # Columnas visibles en el listado
    search_fields = ('cliente__nombre',) # Permite buscar pedidos por nombre de cliente