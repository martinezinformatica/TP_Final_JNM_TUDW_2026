from rest_framework import serializers
from .models import Producto, Pedido, ItemPedido, Mesa

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

class ItemPedidoSerializer(serializers.ModelSerializer):
    # Esto traerá el nombre del producto en lugar de solo el ID
    nombre_producto = serializers.ReadOnlyField(source='producto.nombre')
    
    class Meta:
        model = ItemPedido
        fields = ['id', 'producto', 'nombre_producto', 'cantidad', 'observacion']

class PedidoSerializer(serializers.ModelSerializer):
    items = ItemPedidoSerializer(many=True, read_only=True)
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)

    class Meta:
        model = Pedido
        fields = ['id', 'mesa', 'fecha_creacion', 'estado', 'estado_display', 'total', 'items']