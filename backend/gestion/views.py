from rest_framework import viewsets, status, decorators
from rest_framework.response import Response
from django.db import transaction
from .models import Producto, Pedido, ItemPedido, Mesa
from .serializers import ProductoSerializer, PedidoSerializer, MesaSerializer

class ProductoViewSet(viewsets.ModelViewSet):
   
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class MesaViewSet(viewsets.ModelViewSet):
    queryset = Mesa.objects.all()
    serializer_class = MesaSerializer

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    

   
    @decorators.action(detail=True, methods=['post'])
    def avanzar_estado(self, request, pk=None):
        pedido = self.get_object()
      
        if pedido.estado == 'NUE':
            pedido.estado = 'PRE'
        elif pedido.estado == 'PRE':
            pedido.estado = 'ENT'
        else:
            return Response({"error": "El pedido ya está entregado"}, status=status.HTTP_400_BAD_REQUEST)
        
        pedido.save()
        return Response({'status': 'ok', 'nuevo_estado': pedido.estado})

    def create(self, request, *args, **kwargs):
        items_data = request.data.get('items', [])
        mesa_numero = request.data.get('mesa')

        try:
            with transaction.atomic():               
                mesa = Mesa.objects.get(numero=mesa_numero)            
               
                pedido = Pedido.objects.filter(mesa=mesa, estado='NUE').first()

                if not pedido:
                    pedido = Pedido.objects.create(mesa=mesa, estado='NUE', total=0)
                
                total_adicional = 0
                for item in items_data:
                    producto = Producto.objects.get(id=item['producto'])
                    cantidad = int(item['cantidad'])
                    
                    if producto.stock < cantidad:
                        raise ValueError(f"Stock insuficiente de {producto.nombre}")

                    producto.stock -= cantidad
                    producto.save()

                    ItemPedido.objects.create(
                        pedido=pedido,
                        producto=producto,
                        cantidad=cantidad,
                        observacion=item.get('observacion', '')
                    )
                    total_adicional += (producto.precio * cantidad)

                pedido.total += total_adicional
                pedido.save()

            return Response(PedidoSerializer(pedido).data, status=status.HTTP_201_CREATED)
        except Mesa.DoesNotExist:
            return Response({"error": "La mesa no existe"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)