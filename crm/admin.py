from django.contrib import admin
from .models import Oportunidad


@admin.register(Oportunidad) # Registra el modelo Oportunidad en el panel de admin
class OportunidadAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'cliente', 'valor_estimado', 'etapa', 'fecha_creacion', 'fecha_cierre') # Columnas visibles en el listado
    search_fields = ('titulo', 'cliente__nombre', 'cliente__nif') # Campos por los que se puede buscar
    list_filter = ('etapa', 'fecha_creacion', 'fecha_cierre') # Filtros laterales en el listado