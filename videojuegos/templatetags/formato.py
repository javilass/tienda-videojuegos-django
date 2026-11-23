"""
Filtro de template propio para mostrar precios en pesos chilenos.
Uso en un template:  {% load formato %}  ...  {{ juego.precio|clp }}   ->  $59.990
"""
from django import template

register = template.Library()


@register.filter
def clp(valor):
    try:
        return '$' + f'{int(valor):,}'.replace(',', '.')
    except (TypeError, ValueError):
        return valor
