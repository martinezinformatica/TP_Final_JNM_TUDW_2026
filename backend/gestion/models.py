from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    permite_comanda_especial = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre

class Pedido(models.Model):
    # Definimos los estados 
    ESTADOS_CHOICES = [
        ('NUE', 'Nuevo'),
        ('CON', 'Confirmado'),
        ('PAG', 'Pagado'),
        ('PRE', 'En preparación'),
        ('LIS', 'Listo'),
        ('ENT', 'Entregado'),
        ('CAN', 'Cancelado'),
    ]

    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=3, choices=ESTADOS_CHOICES, default='NUE')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Pedido {self.id} - Mesa {self.mesa.numero} ({self.get_estado_display()})"

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    observacion = models.TextField(blank=True, null=True) # Para la "Comanda especial" 

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"