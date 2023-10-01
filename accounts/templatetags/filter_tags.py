from django import template
from core.models import Order

register = template.Library()

@register.filter(name='split')
def split(value,key):
    return value.split(key)