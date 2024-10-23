from order.models import Product, OrderItem, Order
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(
        queryset=Order.objects.all(), write_only=True
    )
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), write_only=True
    )

    class Meta:
        model = OrderItem
        fields = ["id", "order", "product", "quantity"]


class OrderSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    items = OrderItemSerializer(many=True, read_only=True)
    total = serializers.ReadOnlyField()

    class Meta:
        model = Order
        fields = ["id", "status", "owner", "created_at", "updated_at", "items", "total"]
