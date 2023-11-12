from django.shortcuts import render
from .models import Product


# Create your views here.
def home(request):
    products = Product.objects.all()
    context = {"products": products}
    return render(request, "pages/index.html", context)


# Create your views here.
def product(request, id):
    product = Product.objects.get(pk=id)
    context = {"product": product}
    return render(request, "pages/product.html", context)
