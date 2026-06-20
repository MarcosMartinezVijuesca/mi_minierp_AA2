from rest_framework import serializers
from core.models import Producto


class ProductoSerializer(serializers.ModelSerializer):
    # Convierte objetos de Django a JSON automáticamente
    stock = serializers.SerializerMethodField() # Define stock como campo calculado, no se devuelve automáticamente

    class Meta:
        model = Producto
        fields = ['id', 'sku', 'nombre', 'precio', 'stock']

    def get_stock(self, obj):
        # Método que se ejecuta para calcular el campo stock
        request = self.context.get('request') # Obtiene la request desde el contexto
        if request and request.user.is_authenticated:
            return obj.stock # Devuelve el stock si el usuario está autenticado
        return None # Si no está autenticado, oculta el stock