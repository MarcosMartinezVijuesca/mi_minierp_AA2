from django.contrib import admin
from .models import Cliente, Producto, EstadoPedido
from ventas.forms import ProductoForm, ClienteForm

"""Formularios de validacion para el admin de Django. Se definen en core/forms.py 
y se utilizan aquí para personalizar la validación de los modelos Producto y Cliente 
en el panel de administración."""


@admin.register(Cliente) # Registra el modelo Cliente en el panel de admin
class ClienteAdmin(admin.ModelAdmin):
    form = ClienteForm # Formulario con validación de email corporativo
    list_display = ('id', 'nif', 'nombre', 'email', 'telefono') # Columnas visibles en el listado
    search_fields = ('nif', 'nombre', 'email') # Campos por los que se puede buscar


@admin.register(Producto) # Registra el modelo Producto en el panel de admin
class ProductoAdmin(admin.ModelAdmin):
    form = ProductoForm # Formulario con validación de stock no negativo
    list_display = ('id', 'sku', 'nombre', 'precio', 'stock') # Columnas visibles en el listado
    search_fields = ('sku', 'nombre') # Campos por los que se puede buscar


@admin.register(EstadoPedido) # Registra el modelo EstadoPedido en el panel de admin
class EstadoPedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre') # Columnas visibles en el listado
    search_fields = ('nombre',) # Campos por los que se puede buscar