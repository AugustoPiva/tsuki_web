from django.shortcuts import render,get_object_or_404
from django.urls import reverse_lazy,reverse
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from .models import Pedidos,Listaprecios,Productosordenados,Tiposdegastos,Gastos
from .forms import FormularioNuevoPedido,Fecha,Filtrargastos,Formulario_del_gasto,Cargagasto
from django.views.generic import (View,TemplateView,
                                ListView,DetailView,
                                CreateView,DeleteView,
                                UpdateView)
from django.db.models import Sum,F,Max
from datetime import datetime,date
from django.shortcuts import redirect
from django.core.paginator import Paginator
import gspread
import time
from oauth2client.service_account import ServiceAccountCredentials
global pedido_max
global gasto_max
global carrito

carrito={}
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
                                                            pedido__fecha__year=date.today().year).order_by("pedido")
    pedidostotales=Pedidos.objects.filter(fecha__day=date.today().day,
                                          fecha__month=date.today().month,
                                          fecha__year=date.today().year).count()
    if request.method == "POST":

        day   = int(request.POST['dia'][8:10])
        month = int(request.POST['dia'][5:7])
        year  = int(request.POST['dia'][0:4])

        return HttpResponseRedirect(reverse('tsuki_app:filtrarporfecha',args=(day,month,year)))


    carrito.clear()
    x=date.today()
    fecha=Fecha({'dia':x})

    return render(request,'tsuki_app/pedidos_list.html',{'pedidostotales':pedidostotales,'x':x,'fecha':fecha,'productosdeordenes':productosdelasordenes})

def filtrarfecha(request,**kwargs):

    x= datetime(kwargs['year'],kwargs['month'],kwargs['day'])
    fecha=Fecha({'dia':x})
    productosdelasordenes=Productosordenados.objects.filter(pedido__fecha__day=kwargs['day'],
                                                            pedido__fecha__month=kwargs['month'],
                                                            pedido__fecha__year=kwargs['year'])
    pedidostotales=Pedidos.objects.filter(fecha__day=kwargs['day'],
                                          fecha__month=kwargs['month'],
                                          fecha__year=kwargs['year']).count()
    if request.method == "POST":
        day   = int(request.POST['dia'][8:10])
        month = int(request.POST['dia'][5:7])
        year  = int(request.POST['dia'][0:4])

        return HttpResponseRedirect(reverse('tsuki_app:filtrarporfecha',args=(day,month,year)))

    carrito.clear()
    return render(request,'tsuki_app/pedidos_list.html',{'pedidostotales':pedidostotales,'x':x,'fecha':fecha,'productosdeordenes':productosdelasordenes})

def Index(request):
    return render(request, 'tsuki_app/base.html',{})

def empezarpedido(request):

    productos= Listaprecios.objects.all()
    return render(request,'tsuki_app/nuevo_pedido.html',{'lista':productos,'carro':carrito})

def incorporandoitems(request,producto):

    productos= Listaprecios.objects.all()

    if producto in carrito:
        carrito[producto]= carrito[producto] +  1

    else:
        carrito[producto]=1

    return render(request,'tsuki_app/nuevo_pedido.html',{'lista':productos,'carro':carrito})
        # carrito[producto]=carrito[producto]+1

def eliminarproducto(request,productoaeliminar):

    productos= Listaprecios.objects.all()
    if carrito[productoaeliminar] == 1:
        del carrito[productoaeliminar]
    else:
        carrito[productoaeliminar] = carrito[productoaeliminar]-1

    return render(request,'tsuki_app/nuevo_pedido.html',{'lista':productos,'carro':carrito})

def modificarpedido(request,pk):
    productos= Listaprecios.objects.all()
    orden=Pedidos.objects.get(id=pk)
    carrito=Productosordenados.objects.filter(pedido=pk)
    form = FormularioNuevoPedido(request.POST or None , instance=orden)

    if request.method=="POST" and form.is_valid:
        form.save()
        return redirect('/tsuki_app/')

    return render(request,'tsuki_app/modificar_pedido.html',{'form':form,'lista':productos,'carro':carrito,'orden':orden})

def modificarpedido_quitar(request,pk_pedido,pk_item):
    orden=Pedidos.objects.get(id=pk_pedido)
    form = FormularioNuevoPedido(request.POST or None , instance=orden)
    if request.method=="POST" and form.is_valid:
        form.save()
        return redirect('/tsuki_app/')
    else:
        Productosordenados.objects.get(id=pk_item).delete()
        productos= Listaprecios.objects.all()
        carrito=Productosordenados.objects.filter(pedido=pk_pedido)

        return render(request,'tsuki_app/modificar_pedido.html',{'form':form,'lista':productos,'carro':carrito,'orden':orden})

def modificarpedido_agregar(request,pk_pedido,pk_item):
    carrito=Productosordenados.objects.filter(pedido=pk_pedido)
    orden=Pedidos.objects.get(id=pk_pedido)
    productos= Listaprecios.objects.all()
    form = FormularioNuevoPedido(request.POST or None , instance=orden)

    if request.method=="POST" and form.is_valid:
        form.save()
        return redirect('/tsuki_app/')
    else:
        try:
            product = carrito.get(item=pk_item)
            product.cantidad += 1
            product.save()
        except:
            itemagregar= Listaprecios.objects.get(id=pk_item)
            newproduct = Productosordenados.objects.create(item=itemagregar, pedido=orden)
            newproduct.save()

        return render(request,'tsuki_app/modificar_pedido.html',{'form':form,'lista':productos,'carro':carrito,'orden':orden})

def confirmarpedido(request):

    form = FormularioNuevoPedido(request.POST or None)
    a= Listaprecios.objects.all()
    pedidos= Pedidos.objects.all()

    if request.method == "POST" and form.is_valid():
        form.save()
        ultid= Pedidos.objects.latest('id')
        ultimopedido= Pedidos.objects.get(id=ultid.id)

        for i in carrito:
                prod=get_object_or_404(Listaprecios,id=i)
                order_item = Productosordenados.objects.create(item=prod, cantidad=carrito[i],pedido=ultimopedido)
                order_item.save()

        return HttpResponseRedirect('/tsuki_app/')
    else:
        return render(request, 'tsuki_app/confirmar_pedido.html',{'lista':a,'form':form, 'carro':carrito})

    return render(request,'tsuki_app/confirmar_pedido.html',{'lista':a,'form':form, 'carro':carrito})

def producciondeldia(request,**kwargs):
    productosdelasordenes=Productosordenados.objects.filter(pedido__fecha__day=date.today().day,
                                                            pedido__fecha__month=date.today().month,
                                                            pedido__fecha__year=date.today().year)
    categorias          = ["Clasicos","Simples","Especiales","Premium"]
    tablas              = ["Surtidos","Salmon","Puentes","Barcos"]
    productossinarroz   = ["sugerencia","s_teriyaki","h_langreb","g_tsuki","g_sashimi","g_nigsalm","g_com"]
    totalpiezasporprod  = productosdelasordenes.exclude(item__in=productossinarroz).annotate(total=Sum(F('cantidad') * F('item__cantidad_producto')))
    totalparroz         = totalpiezasporprod.aggregate(supertotal=Sum('total'))['supertotal']
    hotsalmon           = productosdelasordenes.filter(item='h_salm').aggregate(tsalm=Sum('cantidad'))['tsalm']
    hotlangostinos      = productosdelasordenes.filter(item='h_lang').aggregate(tlang=Sum('cantidad'))['tlang']
    langostinosrebozados= productosdelasordenes.filter(item='h_langreb').aggregate(tpinc=Sum('cantidad'))['tpinc']
    rolles              = productosdelasordenes.filter(item__categoria_producto__in=categorias).order_by("item")
    tablas              = productosdelasordenes.filter(item__categoria_producto__in=tablas).order_by("item")

    dict={'totalppp':totalpiezasporprod,
          'totalparroz':totalparroz,
          'productosdelasordenes':productosdelasordenes,
          'hotsalmon':hotsalmon,
          'hotlang':hotlangostinos,
          'lreboz':langostinosrebozados,
          'rolls':rolles,
          'tablas':tablas,
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
            print(objetocreado.id)
            return HttpResponseRedirect(reverse('tsuki_app:presentar_gastos',args=(pk,)))
    return render(request,'tsuki_app/crear_gasto.html',{'form':form})

def iniciobd(request):
    return render(request,'tsuki_app/bd.html',{})

def exportardata(request):
    scope = ['https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('googlesheet.json', scope)
    client = gspread.authorize(creds)
    archivo = client.open("Tsuki")
    sheet_pedidos = archivo.worksheet('Pedidos')
    sheet_gastos  = archivo.worksheet('Gastos')
    sheet_prodordenados = archivo.worksheet('Productos ordenados')
    max_id_pedido = sheet_pedidos.acell('A2').value
    max_id_gasto  = sheet_gastos.acell('A2').value
    max_id_prodordenados  = sheet_prodordenados.acell('A2').value
    pedidos = Pedidos.objects.filter(id__gt=max_id_pedido)
    gastos  = Gastos.objects.filter(id__gt=max_id_gasto)
    prodordenados = Productosordenados.objects.filter(id__gt=max_id_prodordenados)
    lst1=[]
    lst2=[]
    lst3=[]
    for i in pedidos.values():
        for key,value in i.items():
            if key=='fecha':
                lst1.append(str(value))
            else:
                lst1.append(value)
        time.sleep(0.5)
        sheet_pedidos.insert_row(lst1,2)
        lst1=[]
    for a in gastos.values():
        for key,value in a.items():
            if key=='fechacarga':
                lst2.append(str(value))
            else:
                lst2.append(value)
        time.sleep(0.5)
        sheet_gastos.insert_row(lst2,2)
        lst2=[]
    for b in prodordenados.values():
        for key,value in b.items():
                lst3.append(value)
        time.sleep(0.5)
        sheet_prodordenados.insert_row(lst3,2)
        lst3=[]
    return render(request,'tsuki_app/bd.html',{})

def actualizar_carta(request):
    scope = ['https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('googlesheet.json', scope)
    client = gspread.authorize(creds)
    archivo = client.open("Tsuki")
    sheet_listadeprecios = archivo.worksheet('Lista de precios')
    listaprecios = Listaprecios.objects.all()
    lst4=[]
    for i in listaprecios.values():
        for key,value in i.items():
                lst4.append(value)
        time.sleep(1)
        sheet_listadeprecios.insert_row(lst4,2)
        lst4=[]
    return render(request,'tsuki_app/bd.html',{})

def actualizar_listagastos(request):
    scope = ['https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('googlesheet.json', scope)
    client = gspread.authorize(creds)
    archivo = client.open("Tsuki")
    sheet_listadegastos = archivo.worksheet('Lista de gastos')
    listagastos= Tiposdegastos.objects.all()
    lst5=[]
    for i in listagastos.values():
        for key,value in i.items():
                lst5.append(value)
        time.sleep(0.5)
        sheet_listadegastos.insert_row(lst5,2)
        lst5=[]
    return render(request,'tsuki_app/bd.html',{})
