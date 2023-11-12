from django import template


register = template.Library()


@register.filter(name="int_price")
def int_price(value):
    var_1 = str(value)[0 : len(str(value)) - 2]
    var_2 = str(value)[-2:]
    return f"{var_1},{var_2}"
