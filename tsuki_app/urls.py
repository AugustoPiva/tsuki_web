from django.urls import path
from . import views

app_name = 'tsuki_app'

urlpatterns = [
    # en este path se van a ver todos los pedidos del dia
    path('',views.pedidos,name='pedidos'),
    # en este path se van a crear un nuevo pedido
    path('nuevopedido/',views.empezarpedido,name='empezarpedido'),
    path('nuevopedido/<slug:producto>/',views.incorporandoitems,name='incorporando'),
    path('eliminarproducto/<slug:productoaeliminar>/',views.eliminarproducto,name='eliminarproducto'),
    path('confirmarpedido/',views.confirmarpedido ,name='confirmarpedido'),
    path('modificarpedido/<int:pk>/',views.modificarpedido ,name='modificarpedido'),
    path('modificarpedido/agregar/<int:pk_pedido>/<slug:pk_item>/',views.modificarpedido_agregar ,name='agregarproducto'),
    path('modificarpedido/quitar/<int:pk_pedido>/<slug:pk_item>/',views.modificarpedido_quitar ,name='quitarproducto'),
    path('<int:pk>/',views.pedidos,name='eliminarpedido'),
    path('<int:day>/<int:month>/<int:year>/',views.filtrarfecha,name='filtrarporfecha'),
    path('producciondeldia',views.producciondeldia,name='producciondiaria'),
    path('confirmareliminarpedido/<int:pk>/',views.confirmareliminar,name='confirmareliminar'),
    path('cargargasto',views.cargar_gastos,name='cargar_gastos'),
    path('cargargasto/<slug:pk>/',views.cargar_gastos,name='presentar_gastos'),
    path('cargargasto/eliminargasto/<slug:eliminar>',views.cargar_gastos,name='eliminar_gasto'),
    path('cargargasto/creargasto',views.crear_nuevogasto,name='crear_gasto'),
    path('actualizar',views.iniciobd,name='iniciobd'),
    path('actualizar/gastosypedidos',views.exportardata,name='exportardata'),
    path('actualizar/listadeprecios',views.actualizar_carta,name='actualizar_carta'),
    path('actualizar/listadegastos',views.actualizar_listagastos,name='actualizar_listagastos')
#     #asi se asocian las CreatViews.as_view(),name='create'),
#     #si voy a update y al nombre de la pk de la escuela
#     path('update/<int:pk>/',views.SchoolUpdateView.as_view(),name='update'),
#     path('delete/<int:pk>/',views.SchoolDeleteView.as_view(),name='delete')
 ]
