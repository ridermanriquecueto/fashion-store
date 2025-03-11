from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'  # O especifica los campos que quieres incluir
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 5}),  # Ajusta el número de filas del textarea
            'imagen': forms.FileInput(attrs={'class': 'form-control-file'}),  # Añade una clase para estilizar el input de imagen
        }
        labels = {
            'nombre': 'Nombre del Producto',
            'descripcion': 'Descripción',
            'precio': 'Precio',
            'stock': 'Stock',
            'imagen': 'Imagen',
            'categoria': 'Categoría',
        }