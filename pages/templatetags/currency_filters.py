from django import template

register = template.Library()

@register.filter
def cents_to_dollars(value):
    value = float(value)/100
    return value