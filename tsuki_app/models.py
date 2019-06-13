from django.db import models
from django.urls import reverse
from django.conf import settings
from django.db.models import Sum
from datetime import datetime,date

# Create your models here.


class Listaprecios(models.Model):
    id                     = models.SlugField(primary_key = True, max_length =256)
    nombre_producto        = models.CharField(max_length=256,null=True)
    precio_producto        = models.IntegerField(null=True)
    categoria_producto     = models.CharField(max_length=20,null=True)
    cantidad_producto      = models.IntegerField(null=True)
    # subcategoria_producto  = models.CharField(max_length=20,null=True,default=' ')

    def __str__(self):
        return self.nombre_producto

    def get_absolute_url(self):
        return reverse("tsuki_app:incorporando", kwargs={
                'id': self.id
            })

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
                'id': self.id
            })

    def get_remove_from_cart_url(self):
        return reverse("tsuki_app:incorporando", kwargs={
                'id': self.id
            })

class Pedidos(models.Model):
    fecha             = models.DateField(default=date.today)
    nombre_cliente    = models.CharField(max_length=256,null=True)
    comentario        = models.CharField(max_length=256,null=True)

    def __str__(self):
        return self.nombre_cliente

    def get_total(self):
        totaal = 0
        for order_item in Productosordenados.objects.filter(pedido=self.id):
            totaal += order_item.precio_total()
        return totaal

class Productosordenados(models.Model):
# user = models.ForeignKey(Pedidos, on_delete=models.CASCADE)
    # ordered         = models.BooleanField(default=False)
    item            = models.ForeignKey(Listaprecios, on_delete=models.CASCADE)
    pedido          = models.ForeignKey(Pedidos, on_delete=models.CASCADE)
    cantidad        = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.cantidad} - {self.item.nombre_producto}"

    def precio_total(self):
        return self.cantidad * self.item.precio_producto

    def piezas_totales(self):
        return self.cantidad * self.item.cantidad_producto

class Tiposdegastos(models.Model):
    LISTA_CATEGORIAS_GASTOS =[
    ('servicios','Servicios'),
    ('insumos','Insumos'),
    ('mp','Materia prima'),
    ]
    LISTA_MEDICION =[
    ('kg','Kg'),
    ('un','Unidad')
    ]
    descripcion     = models.CharField(max_length=42)
    unidadmedicion  = models.CharField(max_length=30,choices=LISTA_MEDICION)
    categoria       = models.CharField(max_length=40,choices=LISTA_CATEGORIAS_GASTOS)
    stockeable      = models.BooleanField()

    def __str__(self):
        return self.descripcion

class Gastos(models.Model):
    gasto           = models.ForeignKey(Tiposdegastos,on_delete=models.CASCADE)
    cantidades      = models.IntegerField()
    fechacarga      = models.DateField(default=date.today)
    total_gasto     = models.IntegerField(null=True)

    def __str__(self):
        return self.gasto.descripcion
