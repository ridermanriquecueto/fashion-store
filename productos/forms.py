from django import forms
from .models import Producto
from .models import Pedido, MetodoPago, MetodoEntrega, Carrito

class PedidoForm(forms.ModelForm):
    carrito = forms.ModelChoiceField(queryset=Carrito.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    metodo_pago = forms.ModelChoiceField(queryset=MetodoPago.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    metodo_entrega = forms.ModelChoiceField(queryset=MetodoEntrega.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Pedido
        fields = ["cliente", "carrito", "metodo_pago", "metodo_entrega"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Añade clases de Bootstrap a los labels para mejorar la presentación
        self.label_suffix = ""  # Elimina los dos puntos después de las etiquetas
        for field in self.fields.values():
            field.label = field.label.title()  # Capitaliza la primera letra de las etiquetas

    def clean(self):
        cleaned_data = super().clean()
        metodo_pago = cleaned_data.get("metodo_pago")
        metodo_entrega = cleaned_data.get("metodo_entrega")

        if metodo_entrega != "Retiro en Local" and metodo_pago.metodo == "Efectivo en Local":  # Accede al atributo 'metodo' del objeto MetodoPago
            raise forms.ValidationError(
                "El pago en efectivo solo está disponible para retiros en el local. "
                "Selecciona otro método de pago o elige 'Retiro en Local' como método de entrega."
            )

        return cleaned_data
    
    
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        for field in self.fields.values():
            field.label = field.label.title()
            if isinstance(field.widget, forms.FileInput):
                field.widget.attrs.update({'class': 'form-control-file'})
            else:
                field.widget.attrs.update({'class': 'form-control'})
                field.widget.attrs.update({'placeholder': field.label})

            if isinstance(field.widget, forms.Textarea): # Verificación correcta del tipo de widget
                field.widget.attrs['rows'] = 5  # Asignación directa