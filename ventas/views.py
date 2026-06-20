from rest_framework import generics
from core.models import Producto
from .serializers import ProductoSerializer


class ProductoListAPI(generics.ListAPIView):
    queryset = Producto.objects.all().order_by('id') # Ordenado por id
    serializer_class = ProductoSerializer

    def get_serializer_context(self):
        # Sobrescribe para pasar el request al serializer
        context = super().get_serializer_context()
        context['request'] = self.request # Necesario para que el serializer sepa si el usuario está autenticado
        return context