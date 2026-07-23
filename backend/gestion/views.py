from rest_framework import viewsets, status, decorators, views
from rest_framework.response import Response
from django.db import transaction
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Producto, Pedido, ItemPedido, Mesa, CodigoVerificacion
from .serializers import ProductoSerializer, PedidoSerializer, MesaSerializer
from rest_framework.pagination import PageNumberPagination


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer


class MesaViewSet(viewsets.ModelViewSet):
    queryset = Mesa.objects.all()
    serializer_class = MesaSerializer


class HistorialPedidosPagination(PageNumberPagination):
    page_size = 10  

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all().order_by('-fecha_creacion') 
    serializer_class = PedidoSerializer
    pagination_class = HistorialPedidosPagination 

    def paginate_queryset(self, queryset):
        if self.action != 'list':
            return None
        return super().paginate_queryset(queryset)

    @decorators.action(detail=True, methods=['post'])
    def avanzar_estado(self, request, pk=None):
        pedido = self.get_object()

        if pedido.estado == 'NUE':
            pedido.estado = 'PRE'
        elif pedido.estado == 'PRE':
            pedido.estado = 'ENT'
        else:
            return Response(
                {"error": "El pedido esta entregado o cancelado."},
                status=status.HTTP_400_BAD_REQUEST
            )

        pedido.save()
        return Response({'status': 'ok', 'nuevo_estado': pedido.estado})

    def create(self, request, *args, **kwargs):
        items_data = request.data.get('items', [])
        mesa_numero = request.data.get('mesa')

        if mesa_numero is None:
            return Response(
                {"error": "No se especifico ninguna mesa en el pedido."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            with transaction.atomic():                  
                mesa = Mesa.objects.get(id=mesa_numero)
                pedido = Pedido.objects.filter(mesa=mesa, estado='NUE').first()
                if not pedido:
                    pedido = Pedido.objects.create(mesa=mesa, estado='NUE', total=0)
                
                total_adicional = 0
                for item in items_data:
                    producto = Producto.objects.get(id=item['producto'])
                    amount = int(item['cantidad'])

                    if producto.stock < amount:
                        raise ValueError(f"Stock insuficiente para el producto: {producto.nombre}.")                  
                    producto.stock -= amount
                    producto.save()
                   
                    ItemPedido.objects.create(
                        pedido=pedido,
                        producto=producto,
                        cantidad=amount
                    )
                    total_adicional += (producto.precio * amount)

                pedido.total += total_adicional
                pedido.save()

            return Response(PedidoSerializer(pedido).data, status=status.HTTP_201_CREATED)
            
        except Mesa.DoesNotExist:
            return Response(
                {"error": f"La mesa con el numero {mesa_numero} no existe en el sistema."},
                status=status.HTTP_404_NOT_FOUND
            )
        except ValueError as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": "Ocurrio un error al procesar el pedido en el servidor."}, 
                status=status.HTTP_400_BAD_REQUEST
            )


class LoginUnificadoView(views.APIView):
    def post(self, request):
        telefono = request.data.get('telefono', '').strip()

        if not telefono:
            return Response(
                {'error': 'Ingrese su telefono.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(username=telefono)
            rol = 'admin' if (user.is_superuser or user.is_staff) else 'cocina'
            return Response({
                'tipo': 'personal',
                'role': rol,
            }, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            pass

        obj, _ = CodigoVerificacion.objects.get_or_create(telefono=telefono)
        codigo_generado = obj.generar_codigo()
        print(f"\n[WHATSAPP MOCK] Codigo para {telefono}: {codigo_generado}\n")

        return Response({
            'tipo': 'cliente',
            'message': 'Codigo enviado con exito.',
        }, status=status.HTTP_200_OK)


class VerificarCodigoView(views.APIView):
    def post(self, request):
        telefono = request.data.get('telefono', '').strip()
        codigo_ingresado = request.data.get('codigo', '').strip()

        if not telefono or not codigo_ingresado:
            return Response(
                {'error': 'Por favor complete todos los campos.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            registro = CodigoVerificacion.objects.get(telefono=telefono)
        except CodigoVerificacion.DoesNotExist:
            return Response(
                {'error': 'No se solicito un codigo para este telefono.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if registro.codigo != codigo_ingresado:
            return Response(
                {'error': 'El codigo ingresado es incorrecto.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if registro.esta_vencido:
            return Response(
                {'error': 'El codigo ha expirado.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user, _ = User.objects.get_or_create(username=telefono)
        refresh = RefreshToken.for_user(user)        
        registro.delete()

        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'role': 'cliente',
        }, status=status.HTTP_200_OK)


class LoginPersonalView(views.APIView):
    def post(self, request):
        username = request.data.get('username', '').strip()
        password = request.data.get('password', '').strip()

        if not username or not password:
            return Response(
                {'error': 'Complete todos los campos.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            rol = 'admin' if (user.is_superuser or user.is_staff) else 'cocina'
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'role': rol,
            }, status=status.HTTP_200_OK)

        return Response(
            {'error': 'Contraseña incorrecta.'},
            status=status.HTTP_401_UNAUTHORIZED
        )


class SolicitarCodigoView(views.APIView):
    def post(self, request):
        telefono = request.data.get('telefono', '').strip()
        if not telefono:
            return Response(
                {'error': 'Ingrese su telefono.'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        obj, _ = CodigoVerificacion.objects.get_or_create(telefono=telefono)
        codigo_generado = obj.generar_codigo()
        print(f"\n[WHATSAPP MOCK] Re-enviando codigo para {telefono}: {codigo_generado}\n")
        
        return Response({
            'message': 'Codigo enviado con exito.'
        }, status=status.HTTP_200_OK)