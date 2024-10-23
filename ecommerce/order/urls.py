from django.urls import path
from order.views import (
    ProductListView,
    ProductDetailView,
    OrderDetailView,
    OrderListView,
    OrderItemCreateView,
    OrderItemDetailView,
    UserOrderListView,
)

urlpatterns = [
    path("products/", ProductListView.as_view(), name="product-list-create"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
    path("orders/", OrderListView.as_view(), name="order-list-create"),
    path("orders/prev/", UserOrderListView.as_view(), name="order-list"),
    path("order-item/", OrderItemCreateView.as_view(), name="order-item-create"),
    path(
        "orders/<int:user_id>/<int:pk>/", OrderDetailView.as_view(), name="order-detail"
    ),
    path(
        "order-item/<int:order_id>/",
        OrderItemDetailView.as_view(),
        name="order-item-list",
    ),
]
