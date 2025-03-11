from django import template

register = template.Library()

@register.filter(name='multiplicar')  # Nombre del filtro (usado en la plantilla)
def multiplicar(value, arg):
    try:
        return float(value) * float(arg)  # Convierte a float para manejar decimales
    except (ValueError, TypeError):
        return ''  # Maneja errores si los valores no son numéricos

@register.simple_tag(name='total_carrito')  # Sigue siendo un tag
def total_carrito(items_con_total):
    total = sum(item.precio * item.cantidad for item in items_con_total)
    return total