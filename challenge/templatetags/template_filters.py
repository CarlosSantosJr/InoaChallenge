from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    try:
        value = dictionary.get(key)
    except:
        value = "0,00"
    return value