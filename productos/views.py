from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Carrito, ItemCarrito, Pedido
from .forms import ProductoForm, PedidoForm
from django.http import JsonResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import Sum
from django.db import transaction
from django.views.generic import ListView, DetailView, TemplateView  # Importa TemplateView
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt  # Importa csrf_exempt
from .models import Pedido
from django.views.generic import TemplateView 
from django.core.paginator import Paginator

from django.db import connection


def prueba_conexion(request):
    try:
        cursor = connection.cursor()  # Intenta obtener un cursor
        mensaje = "¡Conexión exitosa a la base de datos MySQL!"
    except Exception as e:
        mensaje = f"Error de conexión: {e}"
    return render(request, 'prueba_conexion.html', {'mensaje': mensaje})
def index(request):
    productos = Producto.objects.all()
    productos_destacados = Producto.objects.filter(destacado=True)
    return render(request, 'productos/index.html', {'productos': productos, 'productos_destacados': productos_destacados})


# --- Carrito de compras ---


def total_carrito_ajax(request):
    # Lógica para calcular el total del carrito (ejemplo):
    total_carrito = 0
    if 'carrito' in request.session:
        for item in request.session['carrito'].values():
            total_carrito += float(item['precio']) * item['cantidad']

    return JsonResponse({'total': total_carrito})  # Devuelve el total como JSON


def total_carrito(items):
    total = 0
    if items:  # Verifica si la lista no está vacía
        for item in items:
            try:
                total += float(item.precio) * item.cantidad
            except (ValueError, AttributeError):  # Maneja errores de conversión o atributos faltantes
                pass  # O puedes imprimir un mensaje de error para depuración
    return total

def carrito(request):
    items_con_total = []
    total_carrito = 0

    if 'carrito' in request.session:
        for producto_id, item_data in request.session['carrito'].items():
            try:
                producto = Producto.objects.get(pk=producto_id)
                cantidad = item_data['cantidad']
                precio = float(item_data['precio'])  # Convierte a float aquí
                subtotal = precio * cantidad

                items_con_total.append({
                    'producto': producto,
                    'cantidad': cantidad,
                    'precio': precio,
                    'subtotal': subtotal
                })
                total_carrito += subtotal

            except Producto.DoesNotExist:
                del request.session['carrito'][producto_id]
                request.session.modified = True
                messages.error(request, f"El producto con ID {producto_id} ya no está disponible y fue eliminado del carrito.")
            except (ValueError, TypeError):  # Maneja errores de conversión de precio
                messages.error(request, f"El precio del producto con ID {producto_id} no es válido.")
                continue  # Salta al siguiente producto

    paginator = Paginator(items_con_total, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number) if page_number else paginator.get_page(1)

    context = {
        'page_obj': page_obj,
        'items_con_total': items_con_total,
        'total_carrito': total_carrito,
    }
    return render(request, 'carrito.html', context)


def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    
    item_carrito, created = ItemCarrito.objects.get_or_create(carrito=carrito, producto=producto)
    
    # Si el producto ya existe en el carrito, sumamos la cantidad
    if not created:
        item_carrito.cantidad += 1
    item_carrito.save()
    
    return redirect('catalogo')  # Redirige a

def eliminar_uno(request):
    if request.method == 'POST':
        try:
            producto_id = request.POST.get('producto_id')
            producto_id_str = str(producto_id)

            if producto_id_str in request.session['carrito']:
                if request.session['carrito'][producto_id_str]['cantidad'] > 1:
                    request.session['carrito'][producto_id_str]['cantidad'] -= 1
                else:
                    del request.session['carrito'][producto_id_str]
                request.session.modified = True

                total_carrito = 0
                for item in request.session['carrito'].values():
                    total_carrito += float(item['precio']) * item['cantidad']

                return JsonResponse({'status': 'success', 'total': total_carrito})

            else:
                return JsonResponse({'status': 'error', 'message': 'El producto no está en el carrito.'})

        except KeyError:
            return JsonResponse({'status': 'error', 'message': 'El producto no está en el carrito.'})
        except Exception as e:
            print(f"Error en eliminar_uno: {e}")
            return JsonResponse({'status': 'error', 'message': 'Error inesperado al eliminar el producto.'})

    return JsonResponse({'status': 'error', 'message': 'Método no permitido'})


def actualizar_cantidad(request):
    if request.method == 'POST':
        try:
            producto_id = request.POST.get('producto_id')
            cantidad = int(request.POST.get('cantidad'))

            producto_id_str = str(producto_id)

            if producto_id_str in request.session['carrito']:
                request.session['carrito'][producto_id_str]['cantidad'] = cantidad
                request.session.modified = True

                total_carrito = 0
                for item in request.session['carrito'].values():
                    total_carrito += float(item['precio']) * item['cantidad']

                return JsonResponse({'status': 'success', 'total': total_carrito})
            else:
                return JsonResponse({'status': 'error', 'message': 'El producto no está en el carrito.'})

        except (ValueError, KeyError):
            return JsonResponse({'status': 'error', 'message': 'Cantidad no válida.'})
        except Exception as e:
            print(f"Error en actualizar_cantidad: {e}")
            return JsonResponse({'status': 'error', 'message': 'Error inesperado al actualizar la cantidad.'})

    return JsonResponse({'status': 'error', 'message': 'Método no permitido'})

def eliminar_del_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    # Obtener el carrito (adapta esto a tu lógica)
    carrito_id = request.session.get('carrito_id')  # Intenta obtener el ID del carrito de la sesión
    if carrito_id:
        carrito = Carrito.objects.get(id=carrito_id)
    else:
        # Si no existe un carrito, puedes crear uno nuevo o redirigir a alguna página
        # Ejemplo:
        # carrito = Carrito.objects.create(...)
        # request.session['carrito_id'] = carrito.id
        return redirect('productos:carrito')  # Redirige a la página del carrito

    try:
        item = ItemCarrito.objects.get(producto=producto, carrito=carrito)
        item.delete()
        messages.success(request, f'{producto.nombre} eliminado del carrito.')
    except ItemCarrito.DoesNotExist:
        messages.error(request, f'{producto.nombre} no está en el carrito.')

    return redirect('productos:carrito')

def calcular_total_carrito(request):
    total = 0
    if 'carrito' in request.session:
        for item in request.session['carrito']:
            total += item['precio'] * item['cantidad']
    return total




def eliminar_item(request):
    if request.method == 'POST':
        try:
            producto_id = request.POST.get('producto_id')
            producto_id_str = str(producto_id)

            if producto_id_str in request.session['carrito']:
                del request.session['carrito'][producto_id_str]
                request.session.modified = True

                # Recalcular el total del carrito
                total_carrito = 0
                for item in request.session['carrito'].values():
                    total_carrito += item['precio'] * item['cantidad']

                return JsonResponse({'status': 'success', 'total': total_carrito})  # Devuelve el total actualizado

            else:
                return JsonResponse({'status': 'error', 'message': 'El producto no está en el carrito.'})

        except Exception as e:
            print(f"Error en eliminar_item: {e}")
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Método no permitido'})



def eliminar_todo(request):
    if request.method == 'POST':
        try:
            request.session['carrito'] = {}
            request.session.modified = True
            return JsonResponse({'status': 'success', 'total': 0})  # Devuelve el total como 0

        except Exception as e:
            print(f"Error en eliminar_todo: {e}")
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Método no permitido'})




def finalizar_compra(request):
    if request.method == 'POST':
        try:
            # Lógica para finalizar la compra (ejemplo):
            # 1. Obtener los productos del carrito
            productos_en_carrito = []
            for producto_id, item_data in request.session['carrito'].items():
                producto = Producto.objects.get(pk=producto_id)
                productos_en_carrito.append({
                    'producto': producto,
                    'cantidad': item_data['cantidad'],
                    'precio': item_data['precio']
                })

            # 2. Crear una orden o registro de compra en tu base de datos
            # (Aquí debes adaptar la lógica a tu modelo de Orden)
            # Ejemplo:
            # orden = Orden.objects.create(usuario=request.user, ...)
            # for producto_data in productos_en_carrito:
            #     ItemOrden.objects.create(orden=orden, producto=producto_data['producto'], ...)

            # 3. Limpiar el carrito
            request.session['carrito'] = {}
            request.session.modified = True

            return JsonResponse({'status': 'success'})  # Respuesta JSON exitosa

        except Exception as e:
            print(f"Error al finalizar la compra: {e}")  # Imprime el error para depuración
            return JsonResponse({'status': 'error', 'message': 'Error al finalizar la compra.'})

    return JsonResponse({'status': 'error', 'message': 'Método no permitido'})
##pedidso###

class PedidoView(TemplateView):
    template_name = "productos/pedido.html"

    def get(self, request):  # Para mostrar el formulario en GET
        form = PedidoForm()
        items_con_total = []
        total_carrito = 0

        if 'carrito' in request.session:
            for producto_id, item_data in request.session['carrito'].items():
                try:
                    producto = Producto.objects.get(pk=producto_id)
                    cantidad = item_data['cantidad']
                    precio = float(item_data['precio'])

                    subtotal = precio * cantidad
                    total_carrito += subtotal

                    items_con_total.append({
                        'producto': producto,
                        'cantidad': cantidad,
                        'precio': precio,
                        'subtotal': subtotal
                    })
                except Producto.DoesNotExist:
                    # Manejar el caso en que el producto ya no existe
                    pass

        context = {'form': form, 'items_con_total': items_con_total, 'total_carrito': total_carrito}
        return render(request, self.template_name, context)


    def post(self, request):
        form = PedidoForm(request.POST)  # Instancia el formulario con los datos POST

        if form.is_valid():  # Valida el formulario
            pedido = form.save(commit=False)  # Guarda el pedido pero no lo commite inmediatamente
            # Aquí puedes realizar acciones adicionales antes de guardar el pedido, como:
            # - Asociar el pedido con el usuario actual:
            pedido.cliente = request.user # Asumiendo que tienes un campo 'cliente' en tu modelo Pedido y que el usuario está logueado
            # - Calcular totales, etc. (si no lo haces en el formulario)
            pedido.save()  # Guarda el pedido en la base de datos

            # Limpia el carrito después de la compra.
            if 'carrito' in request.session:
                del request.session['carrito']

            return redirect('pedido_confirmado', pedido_id=pedido.id)  # Redirige a la página de confirmación
        else:
            # Si el formulario no es válido, vuelve a renderizar el formulario con los errores
            items_con_total = []
            total_carrito = 0

            if 'carrito' in request.session:
                for producto_id, item_data in request.session['carrito'].items():
                    try:
                        producto = Producto.objects.get(pk=producto_id)
                        cantidad = item_data['cantidad']
                        precio = float(item_data['precio'])

                        subtotal = precio * cantidad
                        total_carrito += subtotal

                        items_con_total.append({
                            'producto': producto,
                            'cantidad': cantidad,
                            'precio': precio,
                            'subtotal': subtotal
                        })
                    except Producto.DoesNotExist:
                        # Manejar el caso en que el producto ya no existe
                        pass

            context = {'form': form, 'items_con_total': items_con_total, 'total_carrito': total_carrito}
            return render(request, self.template_name, context)


def pedido_exitoso(request):
    return render(request, 'productos/pedido_exitoso.html')

# --- Procesar pedido ---

def confirmar_pedido(request, pedido_id=None):
    if pedido_id:  # Confirmar pedido existente (admin)
        pedido = get_object_or_404(Pedido, id=pedido_id)
        pedido.confirmado = True
        pedido.save()
        messages.success(request, f'Pedido {pedido.id} confirmado.')
        return redirect("productos:lista_pedidos")

    if request.method == 'POST':  # Nuevo pedido (cliente)
        nombre = request.POST['nombre']
        email = request.POST['email']
        direccion = request.POST['direccion']
        metodo_pago = request.POST['metodo_pago']
        metodo_entrega = request.POST['metodo_entrega']

        carrito, _ = Carrito.objects.get_or_create(id=request.session.get('carrito_id'))

        with transaction.atomic():
            for item in carrito.items.all():
                producto = Producto.objects.select_for_update().get(pk=item.producto_id)
                if item.cantidad > producto.stock:
                    messages.error(request, 'Stock insuficiente para completar el pedido.')
                    return render(request, 'productos/carrito.html', {'carrito': carrito})

                producto.stock -= item.cantidad
                producto.save()

            pedido = Pedido.objects.create(
                cliente=nombre,
                carrito=carrito,
                total=carrito.total,
                metodo_pago=metodo_pago,
                metodo_entrega=metodo_entrega
            )

        send_mail(
            'Confirmación de Pedido',
            f'Gracias {nombre}, tu pedido ha sido recibido y será enviado a {direccion}.',
            'tucorreo@tienda.com',
            [email],
            fail_silently=False,
        )

        carrito.items.clear()
        del request.session['carrito_id']

        messages.success(request, 'Pedido realizado con éxito. ¡Gracias por tu compra!')
        return render(request, 'productos/pedido_exitoso.html')

    return redirect('productos:carrito')

# --- Catálogo ---

def catalogo(request):
    # Obtener todos los productos con paginación
    productos = Producto.objects.all()
    paginator = Paginator(productos, 12)  # Mostrar 12 productos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,  # Pasar el objeto de página al template
        'productos': productos # Pasar la lista de productos al template
    }
    return render(request, 'productos/catalogo.html', {'page_obj': page_obj})


def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    return render(request, 'productos/detalle_producto.html', {'producto': producto})

class DetalleProducto(DetailView):
    model = Producto
    template_name = 'productos/detalle_producto.html'  # Nombre del template
    context_object_name = 'producto'

# --- Gestión de productos (CRUD) ---

class ListaProductos(ListView):  # Vista genérica para listar productos (opcional)
    model = Producto
    template_name = 'productos/lista_producto.html'
    context_object_name = 'productos'
    

def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto creado con éxito.')
            return redirect('productos:lista_producto')
    else:
        form = ProductoForm()
    return render(request, 'productos/crear_producto.html', {'form': form})

def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('productos:lista_producto')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'productos/crear_producto.html', {'form': form})

def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    if request.method == 'POST':
        producto.delete()
        return redirect('productos:lista_productos') # Nombre correcto
    return render(request, 'productos/eliminar_producto.html', {'producto': producto})

# --- Gestión de pedidos ---

def lista_pedidos(request):
    pedidos = Pedido.objects.all().order_by("-fecha")
    return render(request, "productos/lista_pedidos.html", {"pedidos": pedidos})

def confirmar_pedido(request, pedido_id=None):
    if pedido_id:
        pedido = get_object_or_404(Pedido, id=pedido_id)
        pedido.confirmado = True
        pedido.save()
        messages.success(request, f'Pedido {pedido.id} confirmado.')
        return redirect("productos:lista_pedidos")

    return redirect('productos:procesar_pedido') # Redirige al método procesar_pedido

# views.py
def eliminar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, pk=pedido_id)  # Obtener el pedido
    if request.method == 'POST':
        pedido.delete()  # Eliminar el pedido
        messages.success(request, 'Pedido eliminado con éxito.')
        return redirect('productos:lista_pedidos')
    return render(request, 'pedidos/confirmar_eliminar.html', {'pedido': pedido})
    confirmación

from django.shortcuts import render

def contacto(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        mensaje = request.POST.get('mensaje')

        # Aquí puedes agregar la lógica para enviar el correo electrónico o guardar el mensaje en la base de datos.

        messages.success(request, '¡Gracias por tu mensaje! Nos pondremos en contacto contigo pronto.')
        return redirect('productos:contacto')  # Redirige a la página de contacto para evitar el reenvío del formulario

    return render(request, 'productos/contacto.html')   
from django.views.generic import TemplateView

class MiVista(TemplateView):
    template_name = "productos/mi_template.html"  # <--- Ruta relativa a la carpeta templates

    #pedidos#
def lista_pedidos(request):
    pedidos = Pedido.objects.all()
    return render(request, 'pedidos/lista_pedidos.html', {'pedidos': pedidos})

def eliminar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, pk=pedido_id)
    if request.method == 'POST':
        pedido.delete()
        return redirect('lista_pedidos')
    return render(request, 'pedidos/confirmar_eliminar.html', {'pedido': pedido})

def confirmar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, pk=pedido_id)
    if request.method == 'POST':
        pedido.confirmado = True  # Marca el pedido como confirmado
        pedido.save()
        return redirect('lista_pedidos')
    return render(request, 'pedidos/confirmar_pedido.html', {'pedido': pedido})  
def pedido(request):  # Define la función 'pedido'
    # Lógica de la vista
    return render(request, 'productos/pedido.html')  
def finalizar_compra(request):
    # Lógica para finalizar la compra
    return render(request, 'productos:finalizar_compra.html') 

def procesar_pago(request):
    if request.method == 'POST':
        # ... (obtener información de la compra desde la sesión) ...

        orden = Orden.objects.create(usuario=request.user, total=total_carrito, metodo_pago='transferencia')

        for item_data in productos_en_carrito:
            ItemOrden.objects.create(orden=orden, producto=item_data['producto'], cantidad=item_data['cantidad'], precio=item_data['precio'])

        # ... (generar datos de la cuenta bancaria) ...

        messages.success(request, 'Para completar la compra, realiza una transferencia a la siguiente cuenta: ...')
        return redirect('productos:detalle_orden', orden.id)  # Redirige a la página de detalles de la orden

    return render(request, 'procesar_pago.html')