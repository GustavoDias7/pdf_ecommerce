from django import template
from django.conf import settings

register = template.Library()


@register.filter(name="cents_price")
def cents_price(value):
    cents = int(value) / 100
    return f"{cents:.2f}".replace(".", ",")


@register.filter(name="get_setting_var")
def get_setting_var(var=""):
    return getattr(settings, var, "")
