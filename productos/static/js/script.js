const botonesDetalle = document.querySelectorAll('.btn-detalle');
botonesDetalle.forEach(boton => {
    boton.addEventListener('click', () => {
        const productoId = boton.dataset.productoId;

        fetch(`/producto/${productoId}/`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                document.getElementById('nombreProducto').textContent = data.nombre;
                document.getElementById('imagenProducto').src = data.imagen;
                document.getElementById('descripcionProducto').textContent = data.descripcion;
                document.getElementById('precioProducto').textContent = data.precio;
            })
            .catch(error => {
                console.error("Error fetching product details:", error);
                alert("Ocurrió un error al cargar los detalles del producto. Inténtalo de nuevo más tarde."); // O un mensaje en un div específico
            });
    });
});

const botonesAgregar = document.querySelectorAll('.btn-agregar');
botonesAgregar.forEach(boton => {
    boton.addEventListener('click', () => {
        const productoId = boton.dataset.productoId;
        const cantidad = document.getElementById(`cantidadProducto${productoId}`).value;

        fetch('/agregar_al_carrito/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify({ producto_id: productoId, cantidad: cantidad })
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if (data.status === 'success') {
                    document.getElementById('cantidadCarrito').textContent = data.cantidad_carrito;
                } else {
                    alert(data.message); // O un mensaje en un div específico
                }
            })
            .catch(error => {
                console.error("Error adding to cart:", error);
                alert("Ocurrió un error al agregar el producto al carrito. Inténtalo de nuevo más tarde."); // O un mensaje en un div específico
            });
    });
});