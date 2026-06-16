from rest_framework import viewsets, status, decorators, views
from rest_framework.response import Response
from django.db import transaction
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Producto, Pedido, ItemPedido, Mesa, CodigoVerificacion
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
                    amount = int(item['cantidad'])
                    
                    if producto.stock < amount:
                        raise ValueError(f"Stock insuficiente de {producto.nombre}")

                    producto.stock -= amount
                    producto.save()

                    ItemPedido.objects.create(
                        pedido=pedido,
                        producto=producto,
                        cantidad=amount,
                        observacion=item.get('observacion', '')
                    )
                    total_adicional += (producto.precio * amount)

                pedido.total += total_adicional
                pedido.save()

            return Response(PedidoSerializer(pedido).data, status=status.HTTP_201_CREATED)
        except Mesa.DoesNotExist:
            return Response({"error": "La mesa no existe"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class SolicitarCodigoView(views.APIView):
    def post(self, request):
        telefono = request.data.get('telefono')
        if not telefono:
            return Response({'error': 'El teléfono es requerido.'}, status=status.HTTP_400_BAD_REQUEST)
        
        obj, created = CodigoVerificacion.objects.get_or_create(telefono=telefono)
        codigo_generado = obj.generar_codigo()
        
        print(f"\n[WHATSAPP MOCK] Código para {telefono}: {codigo_generado}\n")
        
        return Response({'message': 'Código enviado con éxito.'}, status=status.HTTP_200_OK)

class VerificarCodigoView(views.APIView):
    def post(self, request):
        telefono = request.data.get('telefono')
        codigo_ingresado = request.data.get('codigo')
        
        try:
            registro = CodigoVerificacion.objects.get(telefono=telefono)
        except CodigoVerificacion.DoesNotExist:
            return Response({'error': 'No se solicitó código para este número.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if registro.codigo != codigo_ingresado:
            return Response({'error': 'Código incorrecto.'}, status=status.HTTP_400_BAD_REQUEST)
            
        if registro.esta_vencido:
            return Response({'error': 'El código ha expirado.'}, status=status.HTTP_400_BAD_REQUEST)
            
        user, user_created = User.objects.get_or_create(username=telefono)
        refresh = RefreshToken.for_user(user)
        registro.delete()
        
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'role': 'cliente'
        }, status=status.HTTP_200_OK)

class LoginPersonalView(views.APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            rol = 'admin' if user.is_superuser or user.is_staff else 'cocina'
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'role': rol
            }, status=status.HTTP_200_OK)
        
        return Response({'error': 'Credenciales inválidas.'}, status=status.HTTP_401_UNAUTHORIZED)