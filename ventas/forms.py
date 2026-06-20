from django import forms
from core.models import Cliente, Producto


class ProductoForm(forms.ModelForm):
    # Formulario con validación de stock no negativo
    class Meta:
        model = Producto # Modelo asociado
        fields = ['sku', 'nombre', 'precio', 'stock'] # Campos que aparecen en el formulario
        help_texts = {
            'stock': 'No puede ser inferior a 0.', # Texto de ayuda visible en el formulario
        }

    def clean_stock(self): # Método especial de Django para validar un campo concreto
        stock = self.cleaned_data.get('stock') # Obtiene el valor introducido por el usuario
        if stock is not None and stock < 0: # Si el valor existe y es negativo →
            raise forms.ValidationError("El stock no puede ser inferior a 0.") # ← error
        return stock # Si no, devuelve el valor


class ClienteForm(forms.ModelForm):
    # Formulario con validación de email corporativo
    class Meta:
        model = Cliente # Modelo asociado
        fields = ['nif', 'nombre', 'email', 'telefono'] # Campos del formulario
        help_texts = {
            'email': 'Debe pertenecer al dominio corporativo @empresa.com', # Texto de ayuda
        }

    def clean_email(self): # Método de validación específico del campo email
        email = self.cleaned_data.get('email') # Obtiene el valor introducido
        if not email: # Si el usuario no introduce nada →
            raise forms.ValidationError("El email es obligatorio.") # ← error
        if not email.lower().endswith('@empresa.com'): # Comprueba el dominio en minúsculas
            raise forms.ValidationError(
                "El email debe pertenecer al dominio corporativo @empresa.com."
            ) # ← error si no cumple la regla
        return email # Si no, devuelve el valor