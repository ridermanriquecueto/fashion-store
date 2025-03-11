from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import actualizar_cantidad, eliminar_uno, eliminar_todo, finalizar_compra

app_name = 'productos'  # Namespace para evitar colisiones

urlpatterns = [
    # --- Página principal y detalles ---
    path('', views.index, name='index'),
    path('producto/<int:pk>/', views.DetalleProducto.as_view(), name='detalle_producto'),

    # --- Carrito de compras ---
    path('carrito/', views.carrito, name='carrito'),
    path('eliminar-uno/', eliminar_uno, name='eliminar_uno'),
    path('carrito/actualizar/', views.actualizar_cantidad, name='actualizar_cantidad'),
    path('eliminar-todo/', eliminar_todo, name='eliminar_todo'),
   
    path('actualizar-cantidad/', actualizar_cantidad, name='actualizar_cantidad'),
    path('agregar_al_carrito/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('agregar_al_carrito/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    
    path('eliminar_del_carrito/<int:producto_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('total_carrito_ajax/', views.total_carrito_ajax, name='total_carrito_ajax'),
    path('finalizar_compra/', views.finalizar_compra, name='finalizar_compra'),
    path('eliminar_item/', views.eliminar_item, name='eliminar_item'),

    # --- Procesar pedido ---
    path('confirmar_pedido/', views.confirmar_pedido, name='confirmar_pedido'),  # Para nuevos pedidos
    path('confirmar_pedido/<int:pedido_id>/', views.confirmar_pedido, name='confirmar_pedido_admin'),  # Para confirmar pedidos existentes (admin)

    # --- Gestión de productos (CRUD) ---
    path('lista/', views.ListaProductos.as_view(), name='lista_productos'),
    path('productos/', views.ListaProductos.as_view(), name='lista_producto'),  # Vista genérica para listar
    path('productos/crear/', views.crear_producto, name='crear_producto'),
    path('productos/editar/<int:producto_id>/', views.editar_producto, name='editar_producto'),
    path('productos/eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    path('producto/<int:pk>/', views.detalle_producto, name='detalle_producto'),  # Duplicado eliminado

    # --- Gestión de pedidos ---
    path('pedidos/', views.lista_pedidos, name='lista_pedidos'),
    path('pedidos/eliminar/<int:pedido_id>/', views.eliminar_pedido, name='eliminar_pedido'),
    path('pedidos/confirmar/<int:pedido_id>/', views.confirmar_pedido, name='confirmar_pedido'),
    path('pedido/', views.PedidoView.as_view(), name='pedido'),
    path('pedido_exitoso/', views.pedido_exitoso, name='pedido_exitoso'),
    path('pedido/', views.pedido, name='pedido'),  # Duplicado eliminado

    # --- Catálogo ---
    path('catalogo/', views.catalogo, name='catalogo'),
   
    

    # --- Contacto y pago ---
    path('contacto/', views.contacto, name='contacto'),
    path('procesar_pago/', views.procesar_pago, name='procesar_pago'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
