from django.contrib import admin
from django.urls import path
from ventas.views import ProductoListAPI

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/productos/', ProductoListAPI.as_view(), name='api-productos'),
]