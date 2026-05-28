from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from core.models import Producto
from .serializers import ProductoSerializer


class ProductoListAPI(generics.ListAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticated]