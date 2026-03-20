from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db import transaction
from .models import Producto, Pedido, ItemPedido, Mesa
from .serializers import ProductoSerializer, PedidoSerializer

class ProductoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Esta vista permite que el Frontend (Vue) vea la lista de productos
    y los detalles de uno solo, pero no permite borrarlos ni editarlos
    desde la API por seguridad.
    """
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class PedidoViewSet(viewsets.ModelViewSet):
    """
    Esta vista maneja la creación de pedidos.
    Incluye la lógica de validación de stock y transacciones atómicas.
    """
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

    def create(self, request, *args, **kwargs):
        # 1. Extraemos los datos que envía el cliente desde el Frontend
        items_data = request.data.get('items', [])
        mesa_id = request.data.get('mesa')

        if not items_data:
            return Response({"error": "El pedido no tiene productos"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Iniciamos una transacción: si algo falla, no se guarda nada
            with transaction.atomic():
                # Buscamos la mesa
                mesa = Mesa.objects.get(id=mesa_id)
                
                # Creamos el pedido base (Estado 'NUE' por defecto)
                nuevo_pedido = Pedido.objects.create(mesa=mesa, estado='NUE')
                total_pedido = 0

                for item in items_data:
                    producto = Producto.objects.get(id=item['producto'])
                    cantidad = int(item['cantidad'])

                    # --- VALIDAR DISPONIBILIDAD  ---
                    if producto.stock < cantidad:
                        # Si no hay stock, lanzamos error y la transacción vuelve atrás automáticamente
                        return Response(
                            {"error": f"No hay stock suficiente de {producto.nombre}"},
                            status=status.HTTP_400_BAD_REQUEST
                        )

                    # 2. Restar stock del producto
                    producto.stock -= cantidad
                    producto.save()

                    # 3. Crear el detalle del pedido (ItemPedido)
                    ItemPedido.objects.create(
                        pedido=nuevo_pedido,
                        producto=producto,
                        cantidad=cantidad,
                        observacion=item.get('observacion', '') # Aquí va la "Comanda especial"
                    )
                    
                    # Sumamos al total
                    total_pedido += producto.precio * cantidad

                # 4. Guardamos el total calculado en el pedido
                nuevo_pedido.total = total_pedido
                nuevo_pedido.save()

            # Respondemos al frontend con el pedido ya creado
            serializer = PedidoSerializer(nuevo_pedido)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Mesa.DoesNotExist:
            return Response({"error": "La mesa seleccionada no existe"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)