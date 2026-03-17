from django.contrib import admin
from .models import Producto, Mesa, Pedido, ItemPedido

# Esto permite cargar productos dentro del mismo formulario de Pedido
class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 1

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'mesa', 'estado', 'total', 'fecha_creacion')
    list_filter = ('estado', 'mesa')
    inlines = [ItemPedidoInline]

admin.site.register(Producto)
admin.site.register(Mesa)