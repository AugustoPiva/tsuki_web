from django.contrib import admin
from .models import Listaprecios, Pedidos, Productosordenados, Tiposdegastos, Gastos,Clientes
# Register your models here.
admin.site.register(Listaprecios)
admin.site.register(Clientes)
admin.site.register(Pedidos)
admin.site.register(Productosordenados)
admin.site.register(Gastos)
admin.site.register(Tiposdegastos)
