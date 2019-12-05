from django.contrib import admin
from .models import Listaprecios, Pedidos, Productosordenados, Tiposdegastos, Gastos,Clientes
from import_export.admin import ImportExportModelAdmin
from import_export import resources

class ListapreciosResource(resources.ModelResource):
    class Meta:
        model = Listaprecios

class ListapreciosAdmin(ImportExportModelAdmin):
    resource_class = ListapreciosResource

class PedidosResource(resources.ModelResource):
    class Meta:
        model = Pedidos

class PedidosAdmin(ImportExportModelAdmin):
    resource_class = PedidosResource

class ProductosordenadosResource(resources.ModelResource):
    class Meta:
        model = Productosordenados

class ProductosordenadosAdmin(ImportExportModelAdmin):
    resource_class = ProductosordenadosResource

class ClientesResource(resources.ModelResource):
    class Meta:
        model = Clientes

class ClientesAdmin(ImportExportModelAdmin):
    resource_class = ClientesResource

# Register your models here.
admin.site.register(Listaprecios,ListapreciosAdmin)
admin.site.register(Clientes,ClientesAdmin)
admin.site.register(Pedidos,PedidosAdmin)
admin.site.register(Productosordenados,ProductosordenadosAdmin)
admin.site.register(Gastos)
admin.site.register(Tiposdegastos)
