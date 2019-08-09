from django.urls import path
from . import views

app_name = 'tsuki_app'

urlpatterns = [
    # en este path se van a ver todos los pedidos del dia
    path('',views.pedidos,name='pedidos'),
    path('<int:eliminar>',views.Index,name='cancelarpedido'),
    # en este path se van a crear un nuevo pedido
    path('nuevopedido/',views.nuevo_pedido ,name='nuevopedido'),
    path('nuevopedido/<int:pk_client>',views.nuevo_pedido ,name='nuevopedido'),
    path('agregarproductos/<int:pk_pedido>',views.agregarproductos, name='agregarproductos'),
    path('modificarpedido/<int:pk>/',views.modificarpedido ,name='modificarpedido'),
    path('<int:pk>/',views.pedidos,name='eliminarpedido'),
    path('<int:day>/<int:month>/<int:year>/',views.filtrarfecha,name='filtrarporfecha'),
    path('producciondeldia',views.producciondeldia,name='producciondiaria'),
    path('confirmareliminarpedido/<int:pk>/',views.confirmareliminar,name='confirmareliminar'),
    path('cargargasto',views.cargar_gastos,name='cargar_gastos'),
    path('cargargasto/<slug:pk>/',views.cargar_gastos,name='presentar_gastos'),
    path('cargargasto/eliminargasto/<slug:eliminar>',views.cargar_gastos,name='eliminar_gasto'),
    path('cargargasto/creargasto',views.crear_nuevogasto,name='crear_gasto'),
    path('decision_compra',views.decision_compra,name='soporte_compras'),
    path('decision_compra/<slug:pk>/',views.decision_compra,name='soporte_compras_item'),
    path('deudores_vajilla',views.puentesybarcos,name='puentesybarcos'),
    path('deudores_vajilla/<slug:pk>/',views.puentesybarcos,name='puentesybarcos2'),
 ]
