from django import forms
from core.models import Producto, Cliente


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['sku', 'nombre', 'precio', 'stock']

    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock < 0:
            raise forms.ValidationError("El stock no puede ser negativo.")
        return stock


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nif', 'nombre', 'email', 'telefono']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and '@empresa.com' not in email:
            raise forms.ValidationError(
                "El email debe pertenecer al dominio @empresa.com"
            )
        return email