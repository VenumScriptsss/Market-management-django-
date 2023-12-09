from django import template

register = template.Library()
@register.filter
def index_ing(sequence, position):
    return sequence[position]