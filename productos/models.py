from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)  # Añadido `unique=True` para evitar duplicados

    def __str__(self):
        return self.nombre
class Producto(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    destacado = models.BooleanField(default=False)
    
    COLOR_CHOICES = [
        ('rojo', 'Rojo'),
        ('naranja', 'Naranja'),
        ('amarillo', 'Amarillo'),
        ('verde', 'Verde'),
        ('celeste', 'Celeste'),
        ('azul', 'Azul'),
        ('violeta', 'Violeta'),
        ('rosa', 'Rosa'),
        ('negro', 'Negro'),
        ('blanco', 'Blanco'),
        ('gris', 'Gris'),
        ('marrón', 'Marrón'),
    ]
    color = models.CharField(max_length=20, choices=COLOR_CHOICES, default='rojo')
    
    # Cambiar de CharField a ForeignKey
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')

    def __str__(self):
        return f"{self.nombre} (Stock: {self.stock})"


class Carrito(models.Model):
    usuario = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True) 

class ItemCarrito(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items', null=True, blank=True)

    @property
    def subtotal(self):
        return self.cantidad * self.producto.precio

class MetodoPago(models.Model):
    OPCIONES_PAGO = [
        ("Cuenta DNI", "Cuenta DNI"),
        ("Banco Nación", "Banco Nación"),
        ("Efectivo en Local", "Efectivo en Local"),
    ]
    metodo = models.CharField(max_length=25, choices=OPCIONES_PAGO, unique=True)

    def __str__(self):
        return self.metodo

class MetodoEntrega(models.Model):
    OPCIONES_ENTREGA = [
        ("Retiro en Local", "Retiro en Local"),
        ("Retiro en 526 y 133", "Retiro en 526 y 133"),
        ("Envío dentro de La Plata", "Envío dentro de La Plata (+$8.000)"),
        ("Envío fuera de La Plata", "Envío fuera de La Plata (+$15.000)"),
    ]
    metodo = models.CharField(max_length=30, choices=OPCIONES_ENTREGA, unique=True)

    def __str__(self):
        return self.metodo

class Pedido(models.Model):
    cliente = models.CharField(max_length=255)
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, null=True, blank=True)
    metodo_pago = models.ForeignKey(MetodoPago, on_delete=models.CASCADE)
    metodo_entrega = models.ForeignKey(MetodoEntrega, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    confirmado = models.BooleanField(default=False)

    ESTADO_CHOICES = (
        ('pendiente', 'Pendiente'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    )
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')

    @property
    def total(self):
        return self.carrito.total if self.carrito else 0

    def __str__(self):
        return f"Pedido {self.id} - {self.cliente}"

    def save(self, *args, **kwargs):
        if self._state.adding and self.carrito:
            if hasattr(self.carrito, 'usuario'):
                self.carrito.usuario = None
                self.carrito.save()

        super().save(*args, **kwargs)
