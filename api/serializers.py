from rest_framework import serializers
from core.models import Product


class ProductSerializer(serializers.ModelSerializer):
    image = serializers.CharField(source='get_image', read_only=True)

    class Meta:
        model = Product
        exclude = ["pdf", "archived", "stripe_price_id"]