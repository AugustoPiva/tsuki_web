from django import template
from tsuki_app.models import Pedidos
register =template.Library()


@register.filter(name='tomar_valor')
def tomar_valor(value,key):
     return value.get(key)

@register.filter(name='tomarcomentario')
def tomarcomentariodelpedido(orden):
    return orden.comentario
