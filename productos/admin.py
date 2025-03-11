from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.contrib import messages
from .models import Categoria, Producto

class ProductoAdmin(admin.ModelAdmin):
    # Actualiza el list_display y elimina 'categoria' si no existe en el modelo
    list_display = ('nombre', 'precio', 'mostrar_stock')  # Mostrar el stock resaltado
    list_filter = ()  # Elimina el filtro de 'categoria' si no existe
    search_fields = ('nombre',)

    def mostrar_stock(self, obj):
        """Muestra el stock en rojo si es menor a 5."""
        color = "red" if obj.stock < 5 else "black"
        return format_html('<span style="color: {};">{}</span>', color, obj.stock)

    mostrar_stock.admin_order_field = 'stock'  # Permite ordenar por stock
    mostrar_stock.short_description = 'Stock'

    def get_queryset(self, request):
        """Muestra una advertencia si hay productos con stock bajo."""
        queryset = super().get_queryset(request)
        stock_bajo = queryset.filter(stock__lt=5).exists()

        if stock_bajo:
            messages.warning(request, mark_safe(
                "⚠️ Hay productos con <strong>stock bajo</strong>. Revisa la lista para actualizarlos."
            ))

        return queryset

# Registrar el modelo en el panel de administración
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Categoria)  # Asegúrate de que el modelo Categoria también esté registrado
