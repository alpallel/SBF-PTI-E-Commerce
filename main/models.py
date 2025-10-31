from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator
import uuid


class User(models.Model):
    user_id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    username = models.CharField(max_length=20, unique=True)
    user_password = models.CharField(max_length=20)
    user_picture = models.ImageField(upload_to="users/%Y/%m/%d/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True, blank=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Items(models.Model):
    item_id = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=200)
    item_picture = models.ImageField(upload_to="items/%Y/%m/%d/", blank=True, null=True)
    item_description = models.TextField(blank=True)
    item_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="items")
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))])

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["item_name"]
        verbose_name = "item"
        verbose_name_plural = "items"

    def __str__(self):
        return f"{self.item_name} ({self.price})"


class Cart(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name="cart")
    items = models.ManyToManyField(to=Items, through="CartItem", related_name="carts")

    def __str__(self):
        return f"Cart of {self.user}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    item = models.ForeignKey(Items, on_delete=models.CASCADE, related_name="cart_items")
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])

    class Meta:
        unique_together = ("cart", "item")

    def __str__(self):
        return f"{self.quantity} × {self.item.item_name} in {self.cart}"
