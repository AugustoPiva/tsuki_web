from django.db import models
from django.urls import reverse
from django.conf import settings
from django.db.models import Sum
from datetime import datetime,date

# Create your models here.

class Clientes(models.Model):
    nombre_apellido      = models.CharField(max_length=40,unique=True)
    fecha_creacion       = models.DateField(default=date.today)

    def __str__(self):
        return self.nombre_apellido

class Pedidos(models.Model):

    client            = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    fecha             = models.DateField(default=date.today)
    comentario        = models.CharField(max_length=256,null=True,blank=True)
    fecha_creacion    = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.client.nombre_apellido

    def get_total(self):
        totaal = 0
        for order_item in Productosordenados.objects.filter(pedido=self.id):
            totaal += order_item.precio_total()
        return totaal

class Listaprecios(models.Model):
    LISTA_CATEGORIAS = [
            ('rolls','Rolls'),
            ('calientes','Calientes'),
            ('barcos','Barcos'),
            ('puentes','Puentes'),
            ('bd','Barcos descartables'),
            ('laja','Lajas'),
            ('varios','Varios')
    ]

    SUBLISTA_CATEGORIAS =[
            ('hotroll', 'Hot Rolls'),
            ('otros', 'Otros'),
            ('clasicos','Clasicos'),
            ('especiales','Especiales'),
            ('premiums','Premiums'),
            ('veggies','Veggies'),
            ('salsa','Salsas'),
            ('bocados','Bocados'),
            ('surtido','Surtido'),
            ('salmon','Salmon'),
    ]

    nombre_producto        = models.CharField(max_length=256)
    precio_producto        = models.IntegerField()
    categoria_producto     = models.CharField(max_length=20,choices=LISTA_CATEGORIAS)
    sub_categoria_producto = models.CharField(max_length=20,choices=SUBLISTA_CATEGORIAS)
    cantidad_producto      = models.IntegerField()

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

class Productosordenados(models.Model):
    # user = models.ForeignKey(Pedidos, on_delete=models.CASCADE)
    # ordered         = models.BooleanField(default=False)
    item            = models.ForeignKey(Listaprecios, on_delete=models.DO_NOTHING)
    pedido          = models.ForeignKey(Pedidos, on_delete=models.CASCADE)
    cantidad        = models.IntegerField(default=1)
    lotienen        = models.BooleanField(default=False, null=True)
    total           = models.IntegerField(null=True)
    def __str__(self):
        return f"{self.cantidad} - {self.item.nombre_producto}"

    def precio_total(self):
        return self.cantidad * self.item.precio_producto

    def piezas_totales(self):
        return self.cantidad * self.item.cantidad_producto

class Tiposdegastos(models.Model):
    LISTA_CATEGORIAS_GASTOS =[
    ('servicios','Servicios'),
    ('personal','Personal'),
    ('productos','Productos'),
    ('impuestos','Impuestos'),
    ]
    LISTA_SUB_CATEGORIAS_GASTOS =[
    ('verduleria','Verduleria'),
    ('descartable','Descartables'),
    ('cong/frios','Congelados/Frios'),
    ('secos/conservas','Secos/Conservas'),
    ('otros','Otros'),
    ]
    LISTA_MEDICION =[
    ('kg','Kg'),
    ('un','Unidad')
    ]
    descripcion     = models.CharField(max_length=42)
    unidadmedicion  = models.CharField(max_length=30,choices=LISTA_MEDICION)
    categoria       = models.CharField(max_length=40,choices=LISTA_CATEGORIAS_GASTOS,null=True)
    sub_categoria   = models.CharField(max_length=40,choices=LISTA_SUB_CATEGORIAS_GASTOS,null=True)
    stockeable      = models.BooleanField()

    def __str__(self):
        return self.descripcion

class Gastos(models.Model):
    gasto           = models.ForeignKey(Tiposdegastos,on_delete=models.CASCADE)
    cantidades      = models.DecimalField(max_digits=5, decimal_places=2)
    fechacarga      = models.DateField(default=date.today)
    total_gasto     = models.IntegerField(null=True)

    def __str__(self):
        return self.gasto.descripcion
