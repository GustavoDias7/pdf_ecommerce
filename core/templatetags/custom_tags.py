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


@register.simple_tag
def total_price(cents, discount):
    return cents_price(cents - (cents * discount))


@register.filter(name="payment_status")
def payment_status(v):
    return settings.PAYMENT_STATUS.get(v, "")


@register.filter(name="percent")
def percent(decimal=0.0):
    return int(decimal * 100)
