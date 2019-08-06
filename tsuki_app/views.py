from django.shortcuts import render,get_object_or_404
from django.urls import reverse_lazy,reverse
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from .models import Pedidos,Listaprecios,Productosordenados,Tiposdegastos,Gastos,Clientes
from .forms import FormularioNuevoPedido,Fecha,Filtrargastos,Formulario_del_gasto,Cargagasto,Nuevocliente
from django.views.generic import (View,TemplateView,
                                ListView,DetailView,
                                CreateView,DeleteView,
                                UpdateView)
from django.db.models import Sum,F,Max,Avg,StdDev
from datetime import datetime,date
from django.shortcuts import redirect
from django.core.paginator import Paginator
from itertools import chain
import gspread
import time
import locale
locale.setlocale(locale.LC_ALL, 'es_ES')
from oauth2client.service_account import ServiceAccountCredentials
import json
global pedido_max
global gasto_max

#si queres usar template views
# class PruebaTemplateView(TemplateView):
#     template_name = 'algo.html
#
#     def get_context_data(self, **kwargs):
#         context= super().get_context_data(**kwargs)
#         context['injectme']= 'BASIC INJECTION'
#         return context
#
def pedidos(request,**kwargs):
    productosdelasordenes=Productosordenados.objects.filter(pedido__fecha__day=date.today().day,
                                                            pedido__fecha__month=date.today().month,
                                                            pedido__fecha__year=date.today().year).order_by('pedido__client__nombre_apellido','pedido__id')
    pedidostotales=Pedidos.objects.filter(fecha__day=date.today().day,
                                          fecha__month=date.today().month,
                                          fecha__year=date.today().year).count()
    if request.method == "POST":

        day   = int(request.POST['dia'][8:10])
        month = int(request.POST['dia'][5:7])
        year  = int(request.POST['dia'][0:4])

        return HttpResponseRedirect(reverse('tsuki_app:filtrarporfecha',args=(day,month,year)))

    x=date.today()
    fecha=Fecha({'dia':x})

    return render(request,'tsuki_app/pedidos_list.html',{'pedidostotales':pedidostotales,'x':x,'fecha':fecha,'productosdeordenes':productosdelasordenes})

def filtrarfecha(request,**kwargs):

    x= datetime(kwargs['year'],kwargs['month'],kwargs['day'])
    fecha=Fecha({'dia':x})
    productosdelasordenes=Productosordenados.objects.filter(pedido__fecha__day=kwargs['day'],
                                                            pedido__fecha__month=kwargs['month'],
                                                            pedido__fecha__year=kwargs['year']).order_by('pedido__client__nombre_apellido')
    pedidostotales=Pedidos.objects.filter(fecha__day=kwargs['day'],
                                          fecha__month=kwargs['month'],
                                          fecha__year=kwargs['year']).count()
    if request.method == "POST":
        day   = int(request.POST['dia'][8:10])
        month = int(request.POST['dia'][5:7])
        year  = int(request.POST['dia'][0:4])

        return HttpResponseRedirect(reverse('tsuki_app:filtrarporfecha',args=(day,month,year)))
    return render(request,'tsuki_app/pedidos_list.html',{'pedidostotales':pedidostotales,'x':x,'fecha':fecha,'productosdeordenes':productosdelasordenes})

def Index(request,**kwargs):
    #Elimina el que se cancelo y el cliente, si no tiene ningun pedido
    try:
        id_pedido = kwargs['eliminar']
        ultimo_pedido=Pedidos.objects.get(id=id_pedido)
        cliente = Clientes.objects.get(id=ultimo_pedido.client.id)
        Pedidos.objects.get(id=id_pedido).delete()
        carrito.clear()
        if Pedidos.objects.filter(client=cliente).count()==0:
            cliente.delete()
        else:
            pass
    except:
        pass
    return render(request, 'tsuki_app/base.html',{})

def nuevo_pedido(request,**kwargs):
    #Si el cliente esta en la lista de cliente lo elijo y creo un nuevo pedido

    if request.method == "POST":
        if 'Form1' in request.POST:
            form = FormularioNuevoPedido(request.POST or None)
            if form.is_valid:
                form.save()
                pk_pedido= Pedidos.objects.latest('id').id
                return HttpResponseRedirect(reverse('tsuki_app:agregarproductos',args=(pk_pedido,)))
        else:
            form2 = Nuevocliente(request.POST or None)
            if form2.is_valid:
                form2.save()
                pk_client=Clientes.objects.latest('id').id
                return HttpResponseRedirect(reverse('tsuki_app:nuevopedido',args=(pk_client,)))
    else:
        x=date.today()
        form = FormularioNuevoPedido()
        form2 = Nuevocliente(None)
        #si no, creo un nuevo cliente, y automaticamente al crearlo me lo asigna para el proximo pedido
        try:
            cliente_reciencreado=Clientes.objects.get(id=kwargs['pk_client'])
            form=FormularioNuevoPedido({'client':cliente_reciencreado,'fecha':x})
        except:
            pass
        return render(request, 'tsuki_app/nuevo_pedido.html',{'form':form,'form2':form2})

def agregarproductos(request,**kwargs):
    productos= Listaprecios.objects.all()
    ped=kwargs['pk_pedido']
    pedido=Pedidos.objects.get(id=ped)
    if request.method =="POST":
        if request.POST['Productos'] !='{}':
            productos_ordenados=json.loads(request.POST['Productos'])
            for i in productos_ordenados:
                prod=get_object_or_404(Listaprecios,id=i)
                order_item = Productosordenados.objects.create(item=prod,cantidad=productos_ordenados[i],pedido=pedido)
                order_item.save()
            return redirect('/tsuki_app/')
        else:
            pass
    return render(request,'tsuki_app/agregar_productos.html',{'lista':productos,'pedido':pedido})

def modificarpedido(request,pk):
    productos= Listaprecios.objects.all()
    orden=Pedidos.objects.get(id=pk)
    carrito=Productosordenados.objects.filter(pedido=pk)
    # extraigo todos los codigos que tiene la orden actual con sus cantidades en el dict orden_Actual
    orden_actual=list(carrito.values('item__id','cantidad').values_list('item__id','cantidad'))
    #Cargo el formulario con info del cliente, comentario y fecha
    form = FormularioNuevoPedido(request.POST or None , instance=orden)
    if request.method=="POST" and form.is_valid:
        productos_ordenados=json.loads(request.POST['Productos'])
        #si la lista ni se toco no se modifica nada
        if productos_ordenados=={}:
            pass
        else:
            #consulto todos los productos de la orden actual para chequear modificaciones en cantidad o si fueron eliminados
            for prod in orden_actual:
                    # si prod sigue estando en la orden actual...
                if str(prod[0]) in productos_ordenados:
                    #...y si coinciden las cantidades, no modifico nada y (*)
                    if prod[1]==productos_ordenados[str(prod[0])]:
                        pass
                    #si no coinciden actualizo valores
                    else:
                        prod_a_actualizar=Productosordenados.objects.get(pedido__id=pk,item__id=prod[0])
                        prod_a_actualizar.cantidad=productos_ordenados[str(prod[0])]
                        prod_a_actualizar.save()
                #...(*)lo descarto para crear un nuevo producto pedido
                    productos_ordenados.pop(str(prod[0]), None)
                #si no existe lo elimino
                else:
                    instancia=Listaprecios.objects.get(id=prod[0])
                    Productosordenados.objects.get(item=instancia,pedido=orden).delete()
                #luego agrego productos nuevos de productos_ordenados
            for nuevo in productos_ordenados:
                nuevo_producto=get_object_or_404(Listaprecios,id=int(nuevo))
                order_item = Productosordenados.objects.create(item=nuevo_producto,cantidad=productos_ordenados[nuevo],pedido=orden)
        form.save()
        return redirect('/tsuki_app/')
    else:
        pass
    return render(request,'tsuki_app/modificar_pedido.html',{'form':form,'lista':productos,'carro':carrito,'orden':orden})

def producciondeldia(request,**kwargs):
    productosdelasordenes=Productosordenados.objects.filter(pedido__fecha__day=date.today().day,
                                                            pedido__fecha__month=date.today().month,
                                                            pedido__fecha__year=date.today().year)
    tablas              = ["Surtidos","Salmon","Puentes","Barcos"]
    productossinarroz   = ["Sugerencia","Salsa Teriyaki","Langostinos rebozados 3p","Geisha Tsuki 4p","Sashimi 5p","Niguiris de salmon 4p","Niguiris Ahumados 4p","Geisha comun"]
    totalpiezasporprod  = productosdelasordenes.exclude(item__nombre_producto__in=productossinarroz).annotate(total=Sum(F('cantidad') * F('item__cantidad_producto')))
    totalparroz         = totalpiezasporprod.aggregate(supertotal=Sum('total'))['supertotal']
    hotsalmon           = productosdelasordenes.filter(item__nombre_producto='Hot Salmon').aggregate(tsalm=Sum('cantidad'))['tsalm']
    hotlangostinos      = productosdelasordenes.filter(item__nombre_producto='Hot Langostinos').aggregate(tlang=Sum('cantidad'))['tlang']
    langostinosrebozados= productosdelasordenes.filter(item__nombre_producto='Langostinos rebozados 3p').aggregate(tpinc=Sum('cantidad'))['tpinc']
    rolles              = productosdelasordenes.filter(item__categoria_producto='rolls').annotate(Sum('cantidad'))

    dict={'totalppp':totalpiezasporprod,
          'totalparroz':totalparroz,
          'productosdelasordenes':productosdelasordenes,
          'hotsalmon':hotsalmon,
          'hotlang':hotlangostinos,
          'lreboz':langostinosrebozados,
          'rolls':rolles,
    }
    return render(request,'tsuki_app/producciondiaria.html',dict)

def confirmareliminar(request,pk):
    if request.method == "POST":
        Pedidos.objects.get(id=pk).delete()
        return HttpResponseRedirect('/tsuki_app/')
    else:
        s = Pedidos.objects.get(id=pk)
        items =Productosordenados.objects.filter(pedido=pk)
        return render(request,'tsuki_app/confirmareliminacion.html',{'pedidoaeliminar':s,'prods':items})

def cargar_gastos(request,**kwargs):
    gastos_list = Gastos.objects.all().order_by('-fechacarga')
    paginator = Paginator(gastos_list, 8)
    page = request.GET.get('page')
    gastos = paginator.get_page(page)
    form = Filtrargastos()
    formulariocantidad=Cargagasto()
    if request.method == "POST":
        if 'Form1' in request.POST:
            pk=request.POST['seleccionar_gasto']
            return HttpResponseRedirect(reverse('tsuki_app:presentar_gastos',args=(pk)))
        else:
            gasto = Tiposdegastos.objects.get(id=kwargs['pk'])
            pk=kwargs['pk']
            z=request.POST.copy()
            z['gasto']=pk
            formulariocantidad = Cargagasto(z)
            if formulariocantidad.is_valid():
                formulariocantidad.save()
                return HttpResponseRedirect(reverse('tsuki_app:presentar_gastos',args=(pk)))
            else:
                pass
    try:
        gasto = Tiposdegastos.objects.get(id=kwargs['pk'])
        return render(request,'tsuki_app/control_gastos.html',{'gastos':gastos,'form':form,'gasto':gasto,'formulariocantidad':formulariocantidad})
    except:
        pass
    if 'eliminar' in kwargs:
        Gastos.objects.get(id=kwargs['eliminar']).delete()
    else:
        pass
    return render(request,'tsuki_app/control_gastos.html',{'form':form,'gastos':gastos})

def crear_nuevogasto(request):
    form = Formulario_del_gasto(request.POST or None)
    if request.method == 'POST':
        form=Formulario_del_gasto(request.POST)
        if form.is_valid():
            form.save()
            objetocreado=Tiposdegastos.objects.get(descripcion=request.POST['descripcion'])
            pk=objetocreado.id
            return HttpResponseRedirect(reverse('tsuki_app:presentar_gastos',args=(pk,)))
    return render(request,'tsuki_app/crear_gasto.html',{'form':form})

def decision_compra(request,**kwargs):
    def myFunc(e):
        return e['fecha']
    #Brindar las cantidades vendidas de los dias anteriores
    form = Filtrargastos()
    if request.method =='POST':
        pk=request.POST['seleccionar_gasto']
        return HttpResponseRedirect(reverse('tsuki_app:soporte_compras_item',args=(pk)))
    try:
        insumo=Tiposdegastos.objects.get(id=kwargs['pk']).descripcion
        if insumo == "Salmon":
            #agrupamos informacion por fechas con anterioridad a inicios del mes pasado
            piezas_salmon       = Productosordenados.objects.filter(item__sub_categoria_producto='salmon',pedido__fecha__month__gte=datetime.now().month-1).values('pedido__fecha').annotate(total=Sum(F('cantidad')*F('item__cantidad_producto')))
            piezas_sin_salmon   = Productosordenados.objects.filter(item__sub_categoria_producto='surtido',pedido__fecha__month__gte=datetime.now().month-1).values('pedido__fecha').annotate(total=Sum(F('cantidad')*F('item__cantidad_producto'))/2)
            hots_salmon         = Productosordenados.objects.filter(item__nombre_producto='Hot salmon',pedido__fecha__month__gte=datetime.now().month-1).values('pedido__fecha').annotate(total=Sum(F('cantidad')*8))
            # print(piezas_salmon)
            # print(piezas_sin_salmon)
            # print(hots_salmon)
            #piezas_todas_las_fuentes es un objeto que tiene fechas como llaves y las cantidades provenientes de combinados all salmon, sin salmon y hots y rolls
            piezas_todas_las_fuentes=piezas_salmon.union(piezas_sin_salmon,hots_salmon)
            #agrupo por fecha en total_xfecha para eliminar las fuentes y hacer una unica
            total_xfecha= {}
            for i in piezas_todas_las_fuentes:
                if i['pedido__fecha'] in total_xfecha:
                    total_xfecha[i['pedido__fecha']]+=int(i['total'])
                else:
                    total_xfecha[i['pedido__fecha']]=int(i['total'])

             # guardas por fecha una lista de datos a los que llamas--> 1:total piezas salmon del dia,2:dia de la semana,3:numero de la semana
            lista_fecha = []
            for x in total_xfecha:
                lista_fecha.append({'fecha':x,'datos':[total_xfecha[x],x.strftime("%A"),x.isocalendar()[1]]})
            #ordenar de forma ascendente en fecha
            lista_fecha.sort(key=myFunc)
            #separo las cantidades de la semana pasada para generar un cuadro informativo
            pedidos_semana_pasada={'martes':0,'miércoles':0,'jueves':0,'viernes':0,'sábado':0}
            for u in lista_fecha:
                if u['fecha'].isocalendar()[1] == datetime.now().isocalendar()[1]-1:
                    pedidos_semana_pasada[u['fecha'].strftime("%A")]=u['datos'][0]
                else:
                    pass
            form=Filtrargastos()
            print(pedidos_semana_pasada)
            return render(request,'tsuki_app/decision_compra.html',{'form':form,'lista':lista_fecha,'sempas':pedidos_semana_pasada,'insumo':insumo})
    except:
        # reseteo la los pedidos de la semana pasada
        pedidos_semana_pasada={'martes':0,'miércoles':0,'jueves':0,'viernes':0,'sábado':0}
        pass

        insumo = 'sinelegir'
        return render(request,'tsuki_app/decision_compra.html',{'form':form,'insumo':insumo})
