from django.contrib import admin
from . import models
import stripe
from django.conf import settings
from django.contrib import messages


stripe.api_key = settings.STRIPE_SECRET_KEY


@admin.action(description="Create stripe product and price", permissions=["change"])
def create_stripe_product_price(modeladmin, request, queryset):
    if queryset.count() != 1:
        messages.error(request, "Can not create more than one stripe product at once.")
        return
    for query in queryset.values():
        try:
            product_id = str(query["id"])
            product_name = query["name"]
            default_price = {"currency": "BRL", "unit_amount": query["price"]}

            response = stripe.Product.create(
                name=product_name, id=product_id, default_price_data=default_price
            )

            queryset.update(stripe_price_id=response.default_price)
        except Exception as e:
            print(e)
            # Then, when you need to error the user:
            messages.error(request, str(e))


class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "id", "archived"]
    readonly_fields = ["id"]
    fields = [
        "id",
        "name",
        "price",
        "stripe_price_id",
        "description",
        "image",
        "pdf",
        "archived",
    ]
    actions = [create_stripe_product_price]


# Register your models here.
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.User)
