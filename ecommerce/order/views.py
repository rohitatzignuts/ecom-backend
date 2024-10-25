from django.shortcuts import render
from rest_framework import generics
from order.models import Product, Order, OrderItem
from order.serializers import ProductSerializer, OrderItemSerializer, OrderSerializer
from rest_framework import permissions
from order.permissions import IsOwnerOrReadOnly


# Create your views here.
class ProductListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserOrderListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        owner = self.request.user
        return Order.objects.filter(owner=owner).order_by("-created_at")


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        """
        Ensure the user can only retrieve their own orders.
        """
        user_id = self.kwargs["user_id"]
        order_id = self.kwargs["pk"]

        # Return the filtered queryset based on both user and order IDs.
        return OrderItem.objects.filter(order=order_id)


class OrderItemCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


class OrderItemDetailView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderItemSerializer

    def get_queryset(self):
        order_id = self.kwargs["order_id"]
        return OrderItem.objects.filter(order=order_id)
