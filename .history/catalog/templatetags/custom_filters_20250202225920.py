from django import template


register = template.Library()


@register.filter
def mul(value, arg):
    return value * arg

@register.filter
def div(value, arg):
    return value / arg

@register.filter
def sub(value, arg):
    return value - arg

@register.filter
def add(value, arg):
    return value + arg

@register.filter(name='stringify')
def stringify(value):
    return str(value)

@register.filter(name='lower')
def lower(value):
    return value.lower()

@register.filter(name='censor')
def censor_email(email):
    local_part, domain = email.split('@')
    if len(local_part) > 2:
        
    return value
