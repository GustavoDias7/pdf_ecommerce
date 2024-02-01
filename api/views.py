from rest_framework.generics import ListAPIView
from .serializers import ProductSerializer

# from .mypagination import MyCustomPagination
from core.models import Product


class ProductListView(ListAPIView):
    queryset = Product.objects.filter(archived=False)
    serializer_class = ProductSerializer
