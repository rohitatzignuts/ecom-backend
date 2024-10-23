from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
import os


def product_image_path(instance, filename):
    """Generate a file path for new product image upload."""
    return f"products/{instance.name}/{filename}"


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(
        upload_to=product_image_path,
        blank=True,
        null=True,
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    stock = models.PositiveIntegerField(default=10)

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return self.name

    @property
    def image_filename(self):
        """Return just the filename of the uploaded image."""
        if self.image:
            return os.path.basename(self.image.name)
        return None


class OrderItem(models.Model):
    """Through model to link products and orders with quantity."""

    order = models.ForeignKey("Order", on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"


class Order(models.Model):
    OrderStatus = (("PE", "PENDING"), ("CO", "CONFIRMED"), ("CN", "CANCELED"))

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    status = models.CharField(max_length=2, choices=OrderStatus, default="PE")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def __str__(self):
        return f"Order #{self.id} by {self.owner.username}"

    @property
    def total(self):
        """Calculate the total cost of the order."""
        return sum(item.product.price * item.quantity for item in self.items.all())
